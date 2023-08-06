<p align="center">
  <!-- <img src="https://raw.githubusercontent.com/andre-filho/commit-helper/master/assets/200-200.png" style="align: center"> -->
  <h1 align="center">EZIssue</h3>
</p>

<p align="center">
  <a href="https://travis-ci.org/andre-filho/ezissue">
    <img src="https://travis-ci.org/andre-filho/ezissue.svg?branch=master" alt="Build Status">
  </a>
  <!-- <a href="https://codeclimate.com/github/andre-filho/ezissue/maintainability">
    <img src="https://api.codeclimate.com/v1/badges/0ef7545d395120222d77/maintainability" alt="Maintainability">
  </a>
  <a href="https://codebeat.co/projects/github-com-andre-filho-ezissue-master"><img alt="codebeat badge" src="https://codebeat.co/badges/7621c6dc-7143-4efa-af3e-45508210d276" /></a> -->
  <!-- <a href="https://www.codacy.com/app/andre-filho/ezissue?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andre-filho/ezissue&amp;utm_campaign=Badge_Grade">
    <img src="https://api.codacy.com/project/badge/Grade/595af9a088cf44e19ec2679a8c2617f6" alt="Codacy Badge">
  </a> -->
  <!-- <a href="https://codeclimate.com/github/andre-filho/ezissue/test_coverage"><img src="https://api.codeclimate.com/v1/badges/0ef7545d395120222d77/test_coverage" /></a>
  <a class="badge-align" href="https://www.codacy.com/app/andre-filho/ezissue?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andre-filho/ezissue&amp;utm_campaign=Badge_Coverage">
    <img src="https://api.codacy.com/project/badge/Coverage/595af9a088cf44e19ec2679a8c2617f6"/>
  </a> -->
</p>

## What does it do?

The **ezissue cli** is an application with command line interface which it's main objective is to help you
in the issue creation process in your projects.

It takes a file with a markdown table with your issues, formats them and send them to your repo's API.
Therefore you will no longer spend hours creating issues manually.

## Why should I use this?
If you find that the issue creation process is painfull and it breaks your *full-loko* mood while developing something, this is for you.

But if you want to spend hours creating issues on Github or Gitlab and find it fun (I sincerely doubt it), who am I to tell you what to do!

## Usage and configuration

### CLI interface

This program has a CLI that you can take advantage of. Running `ezissue --help`
will show you the usage and options for the CLI.

```bash
$ ezissue --help

  Usage: ezissue [OPTIONS] FILENAME [github|gitlab]

  Options:
    --subid TEXT
    --numerate BOOLEAN
    --prefix [US|TS||BUG]
    --help                 Show this message and exit.
```

### Markdown file and configuration

The EZIssue program takes a `.md` file as argument. That file must have a markdown table for it to parse to issues. That table is a common md table and can have the following headers: (Note that headers with `*` are mandatory, and with `**` are not yet implemented)

| **Header name**     | Description                                                  |          Github support           |                        Gitlab support                        |
| ------------------- | :----------------------------------------------------------- | :-------------------------------: | :----------------------------------------------------------: |
| Title*              | Issue’s title                                                |                 Y                 |                              Y                               |
| Description         | Issue’s body or description                                  |                 Y                 |                              Y                               |
| Tasks               | Will be a list of checkboxes. Items must be separated with commas. |     Y (goes with description)     |                  Y (goes with description)                   |
| Acceptance criteria | Will be a list of checkboxes. Items must be separated with commas. |     Y (goes with description)     |                  Y (goes with description)                   |
| Assignee** | User that is assigned to the issue    |   Y (assignee’s username)   |  N (see next row)  |
| Assignees** | List of users assigned to the issue   | Y (array of assignee’s usernames) |    Y (is a array of user ids)    |
| Labels**  | List of labels that are to be applied to the issue |    Y (array of strings)    | Y (  string, separated by commas) |
| Confidential**    | Toggles the confidentiality of the issue      |    N    |      Y (boolean value)       |
| Milestone**      | Adds a milestone to the issue                |   Y (number of milestone)   |            Y (milestone id)            |
| Due**         | Sets a due date for stressing out your team         |         N         |     Y (datetime string in format `YYYY-MM-DD`)     |
| Discussion**     | Links the issue to a discussion thread            |         N         | Y (id of the discussion that it solves. Fills the description automatically) |
| Weight**       | Sets the issue’s weight. Best used in XP           |         N         | Y (integer with the issue’s weight, must be bigger than zero) |


**Examples:**

The issue output format is the following:

```markdown
 <!-- issue-table.md -->
 | title | description | acceptance criteria |
 | ----- | ----------- | ------------------- |
 | issue title | brief description | condition a;condition b;condition c |
```



```markdown
  <!--title-->
  <PREFIX><SUBID><NUMBER> issue title
  <!--body-->
  **Issue description:**
  ---
  brief description
 
  **Acceptance criteria:**
  ---
  - [ ] condition a
  - [ ] condition b
  - [ ] condition c
```

## Updating your current version

If you already have one of our `pip` releases installed in your machine and want to update to the latest version, use the command:

```bash
$ pip3 install --upgrade ezissue
```

## Want to make a contribuition? Here are some quick stuff you can work on!

I want to thank you beforehand for your contribuition. Here you can find some [quick fixes](https://codebeat.co/projects/github-com-andre-filho-ezissue-development/quick_wins) that you can look into. And be free to ask for new features, solve or add issues in our issue board. :)
