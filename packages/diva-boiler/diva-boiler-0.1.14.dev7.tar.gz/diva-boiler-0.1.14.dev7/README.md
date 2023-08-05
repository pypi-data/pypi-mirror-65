# installation

```bash
# install pipx
python3 -m pip install --user pipx
python3 -m pipx ensurepath

# install boiler tools
pipx install diva-boiler

boiler login
```

# usage

This documentation provides some useful examples, but is not exhaustive.

```bash
# to get up-to-date documentation, use the help option
boiler [noun] --help
boiler [noun] [verb] --help
```

## local data validation

boiler has utilities to validate KW18 data.  These are **offline** operations.

```bash
# show kw18 help
boiler kw18 validate --help

# validate a single set a kw18 files
boiler kw18 validate examples/kw18/minimal

# find and validate all kw18 files recursively
boiler kw18 validate -r examples/kw18
```

For this command, it is assumed that all files associated with a KW18
dataset have the same base name and there is only one `*.kw18` file
per directory.

## searching for videos

```bash
boiler video search --help
boiler video search --name 2018-03-15.10-35-00.10-40-00.school.G336
boiler video search --scenario basketball --gtag G336
```

By default, this command will return only the first 20 matches.  You can get the next
set of results using the `--page` option.
```bash
boiler video search --page 2
```

## downloading annotation data

The following command will download KPF files for one or more videos to the
current directory.  This will fetch the most recent version of all data as
it currently exists in the system (including unaudited annotations).
```bash
boiler export video --help
boiler export video 2018-03-15.10-35-00.10-40-00.school.G336 2018-10-15.17-05-00.17-10-00.alb.G333
```

# video pipeline

## dispatch annotation tasks to vendors

Once a video exists, it can be transitioned to the annotation state.

```bash
boiler vendor dispatch --help

# generate the list of known activity types to file
boiler activity list-types > activity-list.txt

# specify a video, vendor, and list of activities to transition to the annotation stage
boiler vendor dispatch \
  --name kitware \
  --video-name 2999-01-01.00-00-00.00-05-00.admin.G999 \
  --activity-type-list activity-list.txt \
  --set-name test-set
  --annotation-repo-path iMerit/2018-09-06/08/2018-09-06.08-20-00.08-25-00.alb.G229/37-activities
```

Alternatively, the dispatch can be done *after* the results have been returned from the vendor.
This can be done in bulk as follows:

```bash
boiler kw18 dispatch \
  --vendor imerit \
  --set-name testing \
  --activity-type-list activity-list.txt \
  m2-annotations-imerit/iMerit/2018-09-06/*/37-activities
```
This command also support a `--recursive` flag to search recursively for kw18 files under each
listed path.


## vendor activity ingestion

When activities come back from vendors, they should be transitioned to the audit state.

```bash
boiler kw18 ingest --help

# list each directory explicitly to ingest
boiler kw18 ingest m2-annotations-imerit/iMerit/2018-09-06/*/37-activities

# or run recursively
boiler kw18 ingest --recursive m2-annotations-imerit/iMerit
```

Stumpf will first detect whether the files have changed or not.  If they have
not, no further action will be taken.  If they have, then Stumpf will:

1. Generate a transition to the "annotation" status
2. Run server side validation
   * If validation fails, return failure information
   * If validation succeeds, transition to the "audit" state
     and ingest activities from the KW18 files

## audited annotation ingestion

To dispatch videos to gunrunner, use the following command.
```bash
boiler gunrunner dispatch --help
boiler gunrunner dispatch --activity-type-list 47-activities.txt \
  m2-annotations-audit/2018-10-15/08/2018-10-15.08-15-00.08-20-00.alb.G333/47-activities
```
