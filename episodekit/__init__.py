import episodekit.object
import episodekit.episode

__version__ = "0.10.1"

def scan(contextpath, items={}):
  success = True
  success &= episodekit.object.find_all(items, contextpath)
  success &= episodekit.episode.find_all(items, contextpath)

  # if success: # Check for missing dependencies
  for i,it in items.items():
    for dependency in it['depends_on']:
      if dependency not in items:
        print(' * Item {j} (depended on by {i}) is not in the list of found items'.format(i=i, j=dependency))
        success = False

  # if success: # Reverse dependency chain
  for i in items:
    items[i]['depended_on'] = []
  for i in items:
    for d in items[i]['depends_on']:
      if d in items:
        items[d]['depended_on'].append(i)

  if success:
    thinglist = [item for item in items]
    sorted_things = episodekit.utils.sort(thinglist, items)
    for itemid in items: # Sort the depends_on of each thing
      items[itemid]['depends_on'] = [i for i in sorted_things if i in items[itemid]['depends_on']]

  episodekit.utils.ITEMS.clear()
  episodekit.utils.ITEMS.update(items)
  return success
