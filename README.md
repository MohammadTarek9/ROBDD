# ROBDD-Based Equivalence Checker

## Overview
This project implements a **Reduced Ordered Binary Decision Diagram (ROBDD)** based equivalence checker in Python. The tool takes as inputs:

1. **Variable Ordering**: The order in which variables appear in the ROBDD.
2. **Boolean Functions**: Provided in Reverse Polish Notation (RPN) format.

It generates two ROBDDs, saves them into separate files, and determines whether the two Boolean functions are equivalent.
## Input Format
### 1. Variable Ordering
The variable ordering is provided as a space-separated list of variable names (e.g., `x1 x2 x3`).

### 2. Boolean Functions (RPN Format)
Each Boolean function is provided in Reverse Polish Notation (RPN). The operators suppoeted are:
- `AND`
- `OR`
- `NOT`
- `XOR` 
- `NAND` 
- `NOR`
Example: The Boolean expression `(x1 & x2) | x3` is written as `x1 x2 AND x3 OR`.
