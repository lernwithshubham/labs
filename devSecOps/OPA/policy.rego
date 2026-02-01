package play

# By default, deny everything
default allow = false

# Allow becomes true IF...
allow {
    # The input user is "alice"
    input.user == "alice"
    # AND the input action is "read"
    input.action == "read"
}

# OR allow IF...
allow {
    # The user belongs to the "admin" group
    input.groups[_] == "admin"
}
