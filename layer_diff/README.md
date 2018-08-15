# Layer Difference Implementation

This is the basic implementation of the layer difference.
We use the results of the layer split component and compare two different frames.

```
if (std::abs(oldValue - newValue) > thresholdFloat) {
            resultBuffer[i] = newValue;
        }else{
            resultBuffer[i] = 0;
        }
}
```


