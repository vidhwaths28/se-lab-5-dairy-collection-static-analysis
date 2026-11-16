# Reflection

The supplied three-page handout asks for reflection but does not enumerate
reflection questions. These four responses address its stated learning
outcomes and the work completed for this program.

## 1. What did static analysis help identify?

It helped distinguish security defects from behavior and maintainability
problems. In this program, direct SQL construction and shell command execution
were the most serious risks. The analysis also drew attention to weak hashing,
style issues, and code that failed on an empty ledger.

## 2. How did the fixes preserve the program's purpose?

The ledger still records deliveries, totals a day's litres, finds the leading
farmer, lists low-fat or unmeasured deliveries, prints a slip message, and
creates a farmer token. Parameterized SQL protects names containing quotes,
empty queries have defined results, and importing the module no longer runs
the demonstration.

## 3. Which issue mattered most, and why?

Shell execution and SQL interpolation mattered most because input values could
change commands or database operations. Removing the shell call and using
bound SQL parameters reduces those risks while keeping the user-visible
functionality.

## 4. What did this exercise teach about static analysis?

Static analysis catches patterns before a program is run, but its output must
be interpreted in context. It does not prove behavior is correct, so I paired
the analyzer runs with regression tests for quoting, empty data, ranking,
input validation, hash stability, and safe slip printing.
