import React, { useState, useEffect } from "react";
import { View, Text, Button, StyleSheet, ActivityIndicator, Alert } from "react-native";
import { MarketData } from "../market_data";
import { RiskManager } from "../risk_management";
import PushNotification from "react-native-push-notification";

const App = () => {
  const [tradingPerformance, setTradingPerformance] = useState(null);
  const [customizableDashboard, setCustomizableDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const marketData = new MarketData();
    const riskManager = new RiskManager(marketData, 1000, 2);

    const fetchData = async () => {
      try {
        const performanceData = await marketData.getTradingPerformance();
        setTradingPerformance(performanceData);
        
        const dashboardData = await marketData.getCustomizableDashboard();
        setCustomizableDashboard(dashboardData);
      } catch (err) {
        setError("Failed to fetch data. Please try again later.");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handlePushNotification = () => {
    PushNotification.localNotification({
      title: "Trading Alert",
      message: "Check your trading performance!",
      playSound: true,
      soundName: "default",
    });
    Alert.alert("Notification Sent", "Your push notification has been sent!");
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#0000ff" />
        <Text>Loading...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.errorContainer}>
        <Text style={styles.errorText}>{error}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Trading Performance:</Text>
      <Text>{tradingPerformance.metrics}</Text>
      <Text style={styles.title}>Customizable Dashboard:</Text>
      <Text>{customizableDashboard.data}</Text>
      <Button title="Send Push Notification" onPress={handlePushNotification} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    justifyContent: "center",
    alignItems: "center",
  },
  title: {
    fontSize: 20,
    fontWeight: "bold",
    marginVertical: 10,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  errorContainer: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  errorText: {
    color: "red",
    fontSize: 16,
  },
});

export default App;
