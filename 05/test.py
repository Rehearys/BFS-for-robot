from core.application import Application

class Test(Application):

    def initialize(self):
        print("Initializing program ...")

    def update(self):
        pass

# instantiate this classs and run the program
Test().run()
# if __name__ == '__main__':
#     test = Application(screenSize=[1000, 900])
#     test.run()