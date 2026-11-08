#!/usr/bin/env bash
# Run tests, then generate and open the Allure report.
# Usage: ./run_test.sh [pytest args...]   e.g. ./run_test.sh -k test_gd01_002_login_screen
set -u

cd "$(dirname "$0")"

rm -rf allure-results
pytest "$@"
status=$?

if ! command -v allure >/dev/null 2>&1; then
  echo "Allure CLI not found. Install it (macOS: brew install allure) to view the report."
  exit $status
fi

allure generate allure-results --clean --single-file -o allure-report

case "$(uname)" in
  Darwin) open allure-report/index.html ;;
  Linux) xdg-open allure-report/index.html >/dev/null 2>&1 || true ;;
  *) echo "Report: allure-report/index.html" ;;
esac

exit $status
