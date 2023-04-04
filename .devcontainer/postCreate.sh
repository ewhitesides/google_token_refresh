#!/bin/bash

#the following just creates a newline (useful for narrow typing space)
appended_line='PS1="$PS1\n> "'
echo $appended_line >> ~/.bashrc
