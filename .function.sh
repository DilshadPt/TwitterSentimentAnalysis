#!/bin/bash

deployToStable(){

git status;
git fetch --all;
git checkout develop;
git rebase shipit/develop;
git reset --hard $1;
git branch -D stable;
git checkout -b stable;
git push shipit stable -f;
}