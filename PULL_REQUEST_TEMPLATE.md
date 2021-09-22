# Pull Request Template

## Description

Today we implemented a helper function called get_table, which selects tables based on their name. 
This function is called upon in many ways. Instances include:
- View data which updates and goes the first 5000 observations
- deduplicate, which omits duplicates in a table
- Future uses include add_to_use_count(), which will be used to track scripts and their effectiveness. 

This code has eliminated 5 functions in the db.py file while maintaining the integrity of the application. 

This pull request reduces the potential for bugs and adds scalability to the project. 
explanation [video here](https://www.loom.com/share/26629a54700f4c1d89c4ce166377b58d) 


## Type of change

Please delete options that are not relevant.

- [ ] Bug fix (non-breaking change which fixes an issue)
- [x] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] This change requires a documentation update

## How Has This Been Tested?

This has been tested by pulling the first 50 incidents in our data. 

- [x] Test A
- [ ] Test B

**Test Configuration**:
* Firmware version:
* Hardware:
* Toolchain:
* SDK:

## Checklist:

- [x] My code follows the style guidelines of this project
- [x] I have performed a self-review of my own code
- [x] I have commented my code, particularly in hard-to-understand areas
- [x] I have made corresponding changes to the documentation
- [x] My changes generate no new warnings
- [x] I have added tests that prove my fix is effective or that my feature works
- [x] New and existing unit tests pass locally with my changes
- [x] Any dependent changes have been merged and published in downstream modules
- [x] I have checked my code and corrected any misspellings
