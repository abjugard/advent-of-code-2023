import json, re, importlib, sys, os
from time import sleep
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Callable, Iterator
from santas_little_helpers import aoc_root, config
from io import StringIO

aoc_submission_history = aoc_root / '.submission-history'
aoc_response_time_re = re.compile(r'You have ((?P<minutes>[\d]+)m |)(?P<seconds>[\d]+)s left to wait.')
standard_answer_re = re.compile(r'([\d]{4}-[\d]{2}-[\d]{2}) star ([\d]{1}) = (.+)')


def get_submission_history(today: date, level: int):
  if not aoc_submission_history.exists():
    aoc_submission_history.mkdir()
  
  file_path = aoc_submission_history / f'day{today.day:02}.{str(level)}.json'
  if not file_path.exists():
    return dict()

  with file_path.open() as f:
    return json.load(f)


def wait_until(unlock_time):
  while datetime.now() < unlock_time:
    delta = unlock_time - datetime.now()
    print(f'Throttled, waiting {delta.total_seconds()} seconds before retry...', end='\r', flush=True)
    sleep(0.1)
  print()


def __handle_response__(today: date, answer, level, submission_history, text):
  file_path = aoc_submission_history / f'day{today.day:02}.{str(level)}.json'

  response = {
    'timestamp': datetime.now().isoformat()
  }
  
  if 'gave an answer too recently' in text:
    match = aoc_response_time_re.search(text)
    minutes = match.group('minutes')
    seconds = int(match.group('seconds')) + 0.3
    if minutes is not None:
      seconds += 60 * int(minutes)
    unlock_time = datetime.now() + timedelta(seconds=seconds)
    response['unlock_time'] = unlock_time.isoformat()

  if 'not the right answer' in text:
    response['success'] = False
    print(f'Wrong answer', end='')
    hint = None
    if 'too high' in text:
      hint = 'too high'
    if 'too low' in text:
      hint = 'too low'
    if 'right answer for someone else' in text:
      hint = 'correct for another player'
    if hint is not None:
      print(f', hint: {hint}')
      response['hint'] = hint
  elif 'the right answer' in text:
    response['success'] = True
    emoji = '⭐️' if level == 1 else '🌟'
    print(f'Correct answer! {emoji}')
  elif 'finished every puzzle' in text:
    response['success'] = True
    print("🎄 🌟 Advent of Code done, great job! 🌟 🎄")
  elif 'Did you already complete it?' in text:
    response['success'] = True
    answer = 'unknown, see previous attempts'
    print('Correct answer has been submitted already, check the log or the site')
  else:
    print(f'Unrecognised response: {text}')
    response['unknown_text'] = text

  key = str(answer)
  if 'success' not in response:
    key = f'throttled_{response['timestamp']}'
    response['answer'] = answer

  submission_history[key] = response

  with file_path.open('w') as f:
    json.dump(submission_history, f, indent=4)

  if unlock_time is not None:
    wait_until(unlock_time)
    return submit_answer(today, answer, level)
  else:
    return response['success']


def is_solved(submission_history):
  return any(response['success'] == True for response in submission_history.values() if 'success' in response)


def import_requests():
  from requests import request, codes
  from bs4 import BeautifulSoup
  return request, codes, BeautifulSoup


def submit_answer(today: date, answer, level: int = 1, force = False) -> None:
  if not force:
    if type(answer) not in [str, int]:
      print(f'Ignoring answer of type {type(answer)}, submission must be str or int')
      return False
    if answer in ['', 0]:
      print('Ignoring empty answer')
      return False
  if level == 2 and not is_solved(get_submission_history(today, 1)):
    print('Part 1 not solved, refusing to submit part 2')
    return False
  submission_history = get_submission_history(today, level)
  if is_solved(submission_history):
    print(f'Already solved {today} part {level}')
    return True
  if not force:
    if str(answer) in submission_history:
      response = submission_history[str(answer)]
      if 'success' in response:
        print(f"Already tried that at {response['timestamp']}", end='')
        if 'hint' in response:
          print(f", hint was: {response['hint']}", end='')
        print()
        return False
    if len(submission_history) > 0:
      last = max(submission_history.values(), key=lambda x: datetime.fromisoformat(x['timestamp']))
      if 'unlock_time' in last:
        unlock_time = datetime.fromisoformat(last['unlock_time'])
        wait_until(unlock_time)

  request, status_codes, BeautifulSoup = import_requests()
  url = f'https://adventofcode.com/{today.year}/day/{today.day}/answer'
  payload = {'level': level, 'answer': answer}
  res = request('POST', url, cookies=config, data=payload)
  with (aoc_submission_history / 'last_response.html').open('wb') as f2:
    f2.write(res.content)

  soup = BeautifulSoup(res.content, 'html.parser')
  content = soup.find_all('article')[0]
  try:
    return __handle_response__(today, answer, level, submission_history, content.text)
  except Exception:
    print(content.text)
    return False


def restore_stdout():
  sys.stdout = sys.__stdout__


def __submit_output__(theday, output):
  answers = [None, None]
  for line in output.strip().split('\n')[-2:]:
    match = standard_answer_re.match(line)
    if match is None:
      print('Day not formatted using standard format')
      print(line)
      continue
    found_date, level, answer = match.groups()
    assert found_date == str(theday)
    answers[int(level)-1] = answer
  if None in answers:
    print('Missing answers, skipping submit')
    return
  for idx in range(2):
    level = idx + 1
    answer = answers[idx]
    print(f'{theday} star {level}, submitting "{answer}"')
    submit_answer(theday, answer, level)
    if level == 1:
      sleep(6) # there's flood protection between levels


def submit_answers(theday, func):
  with StringIO() as stream:
    sys.stdout = stream
    try:
      func()
      restore_stdout()
      __submit_output__(theday, stream.getvalue())
    except Exception as e:
      restore_stdout()
      print(f'Day {theday} failed to execute')
      return


def __submit_all__():
  for t in reversed(range(1, 6)):
    print(f'About to run and submit all days in {t} seconds...', end='\r', flush=True)
    sleep(1)
  print()
  for file in sorted(Path('.').glob('day[!X]?-*.py')):
    try:
      day = importlib.import_module(file.name[:-3])
    except Exception as e:
      print(f'Failed to import \'{file.name}\': {e}', file=sys.stderr)
      print()
      continue
    all_solved = all(is_solved(get_submission_history(day.today, idx + 1)) for idx in range(2))
    if all_solved:
      print(f'Already solved {day.today} skipping')
      continue
    print(f'Running \'{file.name}\':')
    submit_answers(day.today, day.main)
    print()


if __name__ == '__main__':
  __submit_all__()
