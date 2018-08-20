import hashlib
import sys


def hash_work_unit(wu):
  hasher = hashlib.md5()
  hasher.update(wu.encode('utf-8'))
  return hasher.hexdigest()


def main(fname):
  work_unit = open(fname, mode='r', encoding='utf-8').read()
  retval = hash_work_unit(work_unit)
  with open(fname + "_results", 'w') as fout:
    fout.write(retval)
  with open(fname + "_logs", 'w') as fout:
    fout.write("")


if __name__ == "__main__":
  main(sys.argv[1])
  sys.exit(0)
