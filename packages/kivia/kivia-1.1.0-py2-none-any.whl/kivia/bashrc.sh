#Kivia Package Manager on Bash
command_not_found_handle() {
  kpm \$@
  return 127
}
