import React, { useState } from 'react';
import axios from 'axios';

const App = () => {
    const [videoUrl, setVideoUrl] = useState('');
    const [message, setMessage] = useState('');

    const handleDownload = async () => {
        try {
            setMessage('Pobieranie...');
            // Przesyłamy dane w zgodzie z backendem
            const response = await axios.post('http://127.0.0.1:5000/download', { videoUrl });
            setMessage(response.data.message);
        } catch (error) {
            setMessage(error.response?.data?.error || 'Coś poszło źle');
        }
        setVideoUrl(''); // Ustawienie stanu na pusty ciąg
    };

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>YouTube Downloader</h1>
            <input
                type="text"
                placeholder="Wprowadź Link Do Filmu YT"
                value={videoUrl}
                onChange={(e) => setVideoUrl(e.target.value)} 
                style={{ width: '300px', padding: '10px', marginBottom: '20px' }}
            />
            <br />
            <button onClick={handleDownload} style={{ padding: '10px 20px', cursor: 'pointer' }}>
                Pobierz
            </button>
            <p>{message}</p>
        </div>
    );
};

export default App;
