#%%
import pygal
import pygal_maps_fr

# %%
fr_chart = pygal.maps.fr.Regions(human_readable=True)
fr_chart.title = 'French electricity consumption (in MWh)'
fr_chart.add('In 2019', {
  '28': 5.565, '75': 5.489, '44': 5.302, '76': 5.583, '32': 5.149, '53': 5.208, '93': 6.715, '52': 5.711, '11': 5.664, '27': 5.033, '24': 5.863, '84': 5.715
})
fr_chart.render_in_browser()

