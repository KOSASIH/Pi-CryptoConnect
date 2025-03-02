// src/components/TradingDashboard.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './TradingDashboard.css'; // Importing CSS for styling

const TradingDashboard = () => {
    const [marketData, setMarketData] = useState([]);
    const [selectedPair, setSelectedPair] = useState('PI/USD');
    const [amount, setAmount] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    // Fetch market data from an API
    const fetchMarketData = async () => {
        try {
            const response = await axios.get('/api/marketdata'); // Replace with actual API endpoint
            setMarketData(response.data);
        } catch (err) {
            setError('Failed to fetch market data');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchMarketData();
    }, []);

    const handleTrade = async (type) => {
        setLoading(true);
        setError(null);
        setSuccess(false);

        try {
            const response = await axios.post('/api/trade', {
                pair: selectedPair,
                amount,
                type,
            });
            if (response.status === 200) {
                setSuccess(true);
                setAmount('');
            }
        } catch (err) {
            setError('Trade failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div>Loading market data...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="trading-dashboard">
            <h2>Trading Dashboard</h2>
            <div className="market-data">
                <h3>Market Data</h3>
                <table>
                    <thead>
                        <tr>
                            <th>Pair</th>
                            <th>Price</th>
                            <th>Change</th>
                        </tr>
                    </thead>
                    <tbody>
                        {marketData.map((data) => (
                            <tr key={data.pair} onClick={() => setSelectedPair(data.pair)}>
                                <td>{data.pair}</td>
                                <td>{data.price}</td>
                                <td className={data.change >= 0 ? 'positive' : 'negative'}>
                                    {data.change}%
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div className="trade-form">
                <h3>Trade {selectedPair}</h3>
                <input
                    type="number"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="Amount"
                    required
                />
                <div className="trade-buttons">
                    <button onClick={() => handleTrade('buy')} disabled={loading}>
                        {loading ? 'Processing...' : 'Buy'}
                    </button>
                    <button onClick={() => handleTrade('sell')} disabled={loading}>
                        {loading ? 'Processing...' : 'Sell'}
                    </button>
                </div>
                {success && <div className="success">Trade executed successfully!</div>}
            </div>
        </div>
    );
};

export default TradingDashboard;
