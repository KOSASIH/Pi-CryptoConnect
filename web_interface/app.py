from flask import Flask, render_template, request, jsonify
from pi_cryptoconnect.market_data import MarketData
from pi_cryptoconnect.risk_management import RiskManager

app = Flask(__name__)

market_data = MarketData()
risk_manager = RiskManager(market_data, position_size=1000, risk_reward_ratio=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/trading_performance", methods=["GET"])
def get_trading_performance():
    performance_metrics = market_data.get_trading_performance()
    return jsonify(performance_metrics)

@app.route("/api/customizable_dashboard", methods=["GET"])
def get_customizable_dashboard():
    dashboard_data = market_data.get_customizable_dashboard()
    return jsonify(dashboard_data)

@app.route("/api/push_notifications", methods=["POST"])
def send_push_notification():
    notification_data = request.get_json()
    # Implement push notification logic here
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
