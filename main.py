from models.program import Program
from front.app.app_frame import App

if __name__ == "__main__":
    ui = True
    if ui == True:
        App().startApp()
    else:
        Program.execute()
