// src/components/KYCVerification.js

import React, { useState } from 'react';
import axios from 'axios';
import './KYCVerification.css'; // Importing CSS for styling

const KYCVerification = () => {
    const [formData, setFormData] = useState({
        fullName: '',
        email: '',
        phone: '',
        idNumber: '',
        document: null,
    });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: value,
        }));
    };

    const handleFileChange = (e) => {
        setFormData((prevData) => ({
            ...prevData,
            document: e.target.files[0],
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setSuccess(false);

        const formDataToSend = new FormData();
        for (const key in formData) {
            formDataToSend.append(key, formData[key]);
        }

        try {
            const response = await axios.post('/api/kyc/submit', formDataToSend, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            if (response.status === 200) {
                setSuccess(true);
                setFormData({
                    fullName: '',
                    email: '',
                    phone: '',
                    idNumber: '',
                    document: null,
                });
            }
        } catch (err) {
            setError('Failed to submit KYC data. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="kyc-verification">
            <h2>KYC Verification</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="fullName">Full Name</label>
                    <input
                        type="text"
                        id="fullName"
                        name="fullName"
                        value={formData.fullName}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="email">Email</label>
                    <input
                        type="email"
                        id="email"
                        name="email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="phone">Phone Number</label>
                    <input
                        type="tel"
                        id="phone"
                        name="phone"
                        value={formData.phone}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="idNumber">ID Number</label>
                    <input
                        type="text"
                        id="idNumber"
                        name="idNumber"
                        value={formData.idNumber}
                        onChange={handleChange}
                        required
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="document">Upload Document</label>
                    <input
                        type="file"
                        id="document"
                        name="document"
                        onChange={handleFileChange}
                        required
                    />
                </div>
                <button type="submit" disabled={loading}>
                    {loading ? 'Submitting...' : 'Submit KYC'}
                </button>
            </form>
            {error && <div className="error">{error}</div>}
            {success && <div className="success">KYC submitted successfully!</div>}
        </div>
    );
};

export default KYCVerification;
