from helpers import load_model

def main():
   model_path = "model.xml"  # your actual model file
   model = load_model(model_path)


   print("Loaded in main.py")
   print(model.summary())


if __name__ == "__main__":
   main()
