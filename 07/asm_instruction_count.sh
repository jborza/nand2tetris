#!/bin/bash
cat $1 | grep -v '//' | grep -v '(' | wc -l