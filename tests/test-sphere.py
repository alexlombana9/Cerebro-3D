from vedo import Sphere, Plotter

esfera = Sphere()
esfera.color("green").opacity(0.6)

plotter = Plotter(title="Test Vedo")
plotter.show(esfera, axes=1, viewup="z")
