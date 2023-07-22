from typing import Optional, Dict, List, Union, Tuple
import random
import math


#
# Pick a pixel from a list of buckets
#
# The `position` argument is the position in the virtual pool to be selected.  See the
# docs for `selectRandomPixelWeighted` for information on what this is hand how it
# works
#
# @param {Map<number, [number, number][]>} buckets
# @param {number} position
# @return {[number, number]}
#
def pickFromBuckets(buckets: Dict[int, List], position):
    # All of the buckets, sorted in order from highest priority to lowest priority
    orderedBuckets = [*buckets.items()] # Convert map to array of tuples
    orderedBuckets = sorted(orderedBuckets, key=lambda x: x[0]) # Order by key (priority) ASC
    orderedBuckets = reversed(orderedBuckets) # Order by key (priority) DESC
    orderedBuckets = [l for k, l in orderedBuckets] # Drop the priority, leaving an array of buckets
    
    # list[list[(x: int, y: int)]], inside each bucket is a [x, y] coordinate.
    # Each bucket corresponds to a different prority level.
    
    # Select the position'th element from the buckets
    for bucket in orderedBuckets:
        if len(bucket) <= position:
            position -= len(bucket)
        else:
            return bucket[position]
    
    # If for some reason this breaks, just return a random pixel from the largest bucket
    largestBucket = orderedBuckets[orderedBuckets.index(max(len(b) for b in orderedBuckets))]
    return random.choice(largestBucket)

FOCUS_AREA_SIZE = 75
#
# Select a random pixel weighted by the mask.
#
# The selection algorithm works as follows:
# - Pixels are grouped into buckets based on the mask
# - A virtual pool of {FOCUS_AREA_SIZE} of the highest priority pixels is defined.
#   - If the highest priority bucket contains fewer than FOCUS_AREA_SIZE pixels, the
#     next highest bucket is pulled from, and so on until the $FOCUS_AREA_SIZE pixel
#     threshold is met.
# - A pixel is picked from this virtual pool without any weighting
#
# This algorithm avoids the collision dangers of only using one bucket, while requiring
# no delays, and ensures that the size of the selection pool is always constant.
#
# Another way of looking at this:
# - If >= 75 pixels are missing from the crystal, 100% of the bots will be working there
# - If 50 pixels are missing from the crystal, 67% of the bots will be working there
# - If 25 pixels are missing from the crystal, 33% of the bots will be working there
#
# @param {[number, number][]} diff
# @return {[number, number]}
#
def selectRandomPixelWeighted(diff):
    # Build the buckets
    buckets = {}
    totalAvailablePixels = 0
    for coords in diff:
        (x, y) = coords
        maskValue = int(maskData[x, y, 1]) # brightness of mask coresponds to priority
        if maskValue == 0: continue # zero priority = ignore
        
        totalAvailablePixels += 1
        bucket = buckets.get(maskValue, None)
        if bucket is None:
            buckets[maskValue] = [coords]
        else:
            bucket.append(coords)
    
    # Select from buckets
    # Position represents the index in the virtual pool that we are selecting
    position = math.floor(random.random() * min([FOCUS_AREA_SIZE, totalAvailablePixels]))
    pixel = pickFromBuckets(buckets, position)
    return pixel

#
# Select a random pixel.
#
# @param {[number, number][]} diff
# @return {{x: number, y: number}}
#
