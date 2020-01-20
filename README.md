# Test-Driven Development with Python, Flask, and Docker

[![pipeline status](https://gitlab.com/bashhack/flask-tdd-docker/badges/master/pipeline.svg)](https://gitlab.com/bashhack/flask-tdd-docker/commits/master)

```bash
function on_leave_dir() {
  if [ -e .aliases ]; then
    export OLD_ALIAS_DIR="$PWD"
  fi
}

function on_enter_dir() {
  if [ -n "$OLD_ALIAS_DIR" ] && ! is_subdirectory "$PWD" "$OLD_ALIAS_DIR" ; then
    aliases="$OLD_ALIAS_DIR/.aliases"

    while IFS=':' read -r key value || [ -n "$key" ]; do
      unalias "$key" > /dev/null 2>&1
    done < $aliases

    unset OLD_ALIAS_DIR
    echo "Unloaded local aliases"
  fi

  if [ -e .aliases ]; then
    while IFS=':' read -r key value || [ -n "$key" ]; do
      alias "$key"="${value##*( )}"
    done < ".aliases"

    echo "Loaded local aliases"
  fi
}

function is_subdirectory() {
  local child="$1"
  local parent="$2"
  if [[ "${child##${parent}}" != "$child" ]]; then
    return 0
  else
    return 1
  fi
}

function cd() {
  on_leave_dir
  builtin cd "$@"
  on_enter_dir
}
```
