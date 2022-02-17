# Goal

Understand the photoxicity of various NADH exposures on yeast.


# Plan

With multiple fields of view

```
for each FOV:
    choose an NADH exposure time
    expose
    immediately record a GFP image of MSN2
```


to do this we will need the tools to do varied exposures, so I think using pymmcore-plus is the way to go. Eventually `useq-schema` will probably
be the right tool to define the experiment but may not be there yet. For now do something more bespoke.


# Notes

## 2022-01-24
Going to experiment with demo camera to figure out best way to do this.
