import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Chat from './pages/Chat';

function App() {
    const isAuthenticated = !!localStorage.getItem('token');

    return (
        <Router>
            <div className="min-h-screen bg-background font-sans antialiased">
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route
                        path="/"
                        element={isAuthenticated ? <Chat /> : <Navigate to="/login" />}
                    />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
