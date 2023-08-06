# Changelog

All notable changes to this project will be documented in this file.

## [Ideas]

- Figure out a way, if at all useful, to print more details (software versions; Nmap script output).
- Add more useful parsers?
- Look into grouping similar observations when outputting to XLSX
- Not sure if useful, but look into adding an optional Nessus column to print each finding details.

## [Unreleased]

- None.

## [0.0.22] - 2020-04-10

### Added

- Added SNMP worksheet observations for the Nessus parser.
- Added '--nmap-host-list' argument for the Nmap parser to print all found hosts that have open TCP / UDP ports.

### Changed

- Minor bug fixes in the Nessus parser.

### Removed

- None.

## [0.0.21] - 2020-03-05

### Added

- None.

### Changed

- None.

### Removed

- Removed argparse as a separate dependency.

## [0.0.20] - 2020-02-24

### Added

- Added more HTTP worksheet observations.

## Changed

- None.

## Removed

- None.

## [0.0.19] - 2020-01-27

### Added

- Added SMB, RDP and SSH worksheets for the Nessus parser.

### Changed

- None.

### Removed

- None.

## [0.0.18] - 2020-01-27

### Added

- None.

### Changed

- Fixed a bug that omitted every first item in each of the Critical, High, Medium, Low, Info worksheets.
Fixed a bug that messed up the TLS, X509 and HTTP worksheets.
Fixed a bug that no longer interprets large cells as overly large URLs.

### Removed

- Removed the '--no-nessus-plugin-output' argument for Nessus.
Didn't use it and caused too many exceptions in the code.

## [0.0.17] - 2019-12-28

### Added

- None.

### Changed

- Restructured package a bit.
When not installed as a package, sr2t can be run with 'python -m sr2t' (as opposed to 'python -m sr2t.sr2t').

### Removed

- None.

## [0.0.16] - 2019-12-26

### Added

- Added new argument for Nmap parser to print a supplemental list of detected services, if present in the parsed XML.

### Changed

- None.

### Removed

- None.

## [0.0.15] - 2019-12-26

### Added

- None.

### Changed

- Fixed linter issues.

### Removed

- None.

## [0.0.14] - 2019-12-26

### Added

- Ho ho ho, added arguments to specify your own custom Nessus YAML files for auto classifications, and the Nessus TLS, X.509, and HTTP worksheets.
Have a look at the YAML files in the 'sr2t/data' folder to see how you can create your own custom YAML files.

### Changed

- The Nmap parser will now print both TCP and UDP ports optimistically, if it finds them.
No need to specify '--nmap-protocol' anymore.

### Removed

- Removed the '--nmap-protocol' argument, as there is no need anymore (see the Changed section of this release to see why).

## [0.0.13] - 2019-12-25

### Added

- Ho ho ho, added yamllint to pipeline.

### Changed

- All data files are now refactored into pretty YAML files.

### Removed

- None.

## [0.0.12] - 2019-12-24

### Added

- None.

### Changed

- Moved all testssl.sh findings to match for, to a separate file.

### Removed

- None.

## [0.0.11] - 2019-12-23

### Added

- Added a CHANGELOG.md

### Changed

- Updated README.
- Dirble XLSX worksheet now has a blue color.
- Nessus XLSX SYN, TLS, X.509 and HTTP worksheets no longer contain 'Nessus' in their worksheet names as it's quite obvious, IMHO, and saves space.

### Removed

- None.

## [0.0.10] - 2019-12-23

### Added

- Multiple parsers can now be used in a single run.
When outputting to XLSX, separate worksheets will simply be appended to the same XLSX file.
When outputting to CSV, you should now specify a basename (i.e. no extension).

### Changed

- Updated README.
- .gitlab-ci.yml now lints al Python scripts it can find with flake8, recursively up to 2 child directories.

### Removed

- None.

## [0.0.9] - 2019-12-23

### Added

- Added more auto classifications.

### Changed

- Moved auto classifications etc. to separate files.
- Make X's visible in Nessus worksheets for colour blind people.

### Removed

- None.
