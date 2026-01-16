from flask import Flask, request, jsonify, render_template
import joblib
model = joblib.load("Hotwheelsmodel.pkl")
iris_classes = {0: "Mainlines", 1: "Fantasies", 2: "Hotwheels premium"}
Mainlines_cars= ["Ferrari spyder", "Mustang GTD", "Ford gt","Dodge Viper"]
Fantasies_cars = ["Batomobile", "Crocodile", "Croc road","Shark Bite"]
Hotwheels_premium = ["95 Camaro","78 Porsche","Volkswagen Bettle","Agera r"]
Mainlines_cars_prices = {"Ferrari spyder": 899, "Mustang GTD": 658, "Ford gt": 800, "Dodge Viper": 750}
Fantasies_cars_prices = {"Batomobile": 167, "Crocodile": 167, "Croc road": 167, "Shark Bite": 167}
Hotwheels_premium_prices = {"95 Camaro": 1200, "78 Porsche": 2100, "Volkswagen Bettle": 1500, "Agera r": 2200}
app = Flask(__name__)
@app.route("/Hotwheels")
def Hotwheels():
 return render_template("Hotwheelsindex.html")
@app.route("/Hotwheels", methods=["POST"])
def select():
 try:
     cars = request.form.getlist("cars")
     if not cars:
        return render_template("Hotwheelsindex.html", error="No cars selected")
     
     results = []
     total = 0
     for cars in cars:
        # Determine category based on item
        if cars in Mainlines_cars:
           category = "Mainlines"
           price = Mainlines_cars_prices[cars]
           features = [1, 0, 0, 0]
        elif cars in Fantasies_cars:
           category = "Fantasies"
           price = Fantasies_cars_prices[cars]
           features = [0, 1, 0, 0]
        elif cars in Hotwheels_premium:
           category = "Premiums"
           price =Hotwheels_premium_prices[cars]
           features = [0, 0, 1, 0]
        else:
           return render_template("Hotwheelsindex.html", error=f"Invalid item: {cars}")
        prediction = model.predict([features])
        predicted_category = iris_classes[prediction[0]]
        
        results.append({"item": cars, "category": category, "price": price, "predicted_category": predicted_category})
        total += price
     
     return render_template("bill.html", results=results, total=total)
 except Exception as e:
     return render_template("Hotwheelsindex.html", error=str(e))
if __name__ == "__main__":
 app.run(host="0.0.0.0", port=8080)

