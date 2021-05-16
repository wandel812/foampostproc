from paraview.simple import *
import time

# def print_hi(name):
#
#     case1 = OpenFOAMReader(FileName='/home/dm/openfoam/cavity/a.foam')
#
#     case1.CellArrays = ['U']
#     case1.MeshRegions = ['internalMesh']
#     servermanager.Fetch(case1)
#     pointData = CellDatatoPointData(Input=case1)
#
#     # # create slice
#     # slice1 = Slice(Input=pointData)
#     # slice1.SliceType = "Plane"
#     # slice1.SliceType.Origin = [0.0, 0.0, 0.0]
#     # slice1.SliceType.Normal = [0.0, 0.0, 1.0]
#     # slice1.PointData.GetArray(0)
#
#     # create view
#     view1 = CreateRenderView(pointData)
#     view1.ViewSize = [600,400]
#     view1.InteractionMode = '2D'
#     view1.CameraViewUp = [0.0, 1.0, 1.0]
#     view1.ViewTime = max(case1.TimestepValues)
#     # show view
#     display1 = Show(view1)
#     display1.Visibility = 1
#     display1.ColorArrayName = 'U'
#     display1.LookupTable = GetLookupTableForArray("U", 0)
#
#     # save state
#     # servermanager.SaveState('./elbow.pvsm')
#
#     # render view
#     Render()
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# def test():
#     foamfoam = OpenFOAMReader(FileName='/home/dm/openfoam/cavity/a.foam')
#     foamfoam.MeshRegions = ['internalMesh']
#     servermanager.Fetch(foamfoam)
#     view = CreateRenderView(foamfoam)
#     view.ViewTime = max(foamfoam.TimestepValues)
#     Show(foamfoam, view)
#     #Render(view)
#     SaveScreenshot("aview.png", view)
#
# def test1():
#     source = Sphere()
#     view = CreateRenderView()
#     display = Show(source, view)
#     display.Visibility = 1
#     Render(view)

from pymongo import MongoClient

if __name__ == '__main__':
    # test()
    login = "dbUser"
    password = "a4eYAyhZ4xgXEre"
    db_proj_name = "foampostproc"
    db_connect_link = f"mongodb+srv://{login}:{password}@cluster0.ecqqe.mongodb.net/{db_proj_name}?retryWrites=true&w=majority"
    cluster = MongoClient(db_connect_link)
    db = cluster.foampostproc_db
    collection = db.foamcase
    print(type(collection.find()))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
