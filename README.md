# glu

Glu is a simple tool to allow aid managing multi-repo projects.  For example, say you have several projects in a tree structure:

```

/root
  /foo
    /repo1
    /repo2
  /bar
    /repo3
    /repo4
```

To fetch the latest code you need to navigate to each repository, simply run `glu` from the root repository, with the

```
glu git pull
```

## Arguments

