import { useState } from 'react';
import { Link } from 'react-router-dom';
import api from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '@/components/ui/card';

interface FieldErrors {
    username?: string;
    email?: string;
    password?: string;
    general?: string;
}

export default function Register() {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setErrors] = useState<FieldErrors>({});
    const [loading, setLoading] = useState(false);


    const validateForm = (): boolean => {
        const newErrors: FieldErrors = {};

        if (username.length < 3) {
            newErrors.username = 'Username must be at least 3 characters.';
        } else if (username.length > 50) {
            newErrors.username = 'Username must be 50 characters or less.';
        }

        if (!email) {
            newErrors.email = 'Email is required.';
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            newErrors.email = 'Please enter a valid email address.';
        }

        if (password.length < 6) {
            newErrors.password = 'Password must be at least 6 characters.';
        }

        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();

        // Client-side validation first
        if (!validateForm()) return;

        setLoading(true);
        setErrors({});

        try {
            const response = await api.post('auth/register', { email, username, password });

            const { access_token, user } = response.data;

            localStorage.setItem('token', access_token);
            localStorage.setItem('user', JSON.stringify(user));

            window.location.href = '/';
        } catch (err: any) {
            const detail = err.response?.data?.detail;
            if (typeof detail === 'string') {
                setErrors({ general: detail });
            } else if (Array.isArray(detail)) {
                // Parse FastAPI 422 validation errors into per-field messages
                const fieldErrors: FieldErrors = {};
                for (const item of detail) {
                    // item.loc is like ["body", "username"]
                    const field = item.loc?.[item.loc.length - 1];
                    if (field === 'username' || field === 'email' || field === 'password') {
                        fieldErrors[field] = item.msg;
                    }
                }
                if (Object.keys(fieldErrors).length === 0) {
                    setErrors({ general: detail.map((e: any) => e.msg).join(', ') });
                } else {
                    setErrors(fieldErrors);
                }
            } else {
                setErrors({ general: 'Registration failed. Try simpler or different credentials.' });
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex items-center justify-center min-h-screen bg-gray-50">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle className="text-2xl text-center">Join FashNet</CardTitle>
                </CardHeader>
                <CardContent>
                    <form onSubmit={handleRegister} className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Username</label>
                            <Input
                                type="text"
                                placeholder="StyleGuru"
                                value={username}
                                onChange={(e) => { setUsername(e.target.value); if (errors.username) setErrors(prev => ({ ...prev, username: undefined })); }}
                                required
                            />
                            {errors.username && (
                                <p className="text-xs text-red-500 mt-1">{errors.username}</p>
                            )}
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Email</label>
                            <Input
                                type="email"
                                placeholder="name@example.com"
                                value={email}
                                onChange={(e) => { setEmail(e.target.value); if (errors.email) setErrors(prev => ({ ...prev, email: undefined })); }}
                                required
                            />
                            {errors.email && (
                                <p className="text-xs text-red-500 mt-1">{errors.email}</p>
                            )}
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">Password</label>
                            <Input
                                type="password"
                                placeholder="••••••••"
                                value={password}
                                onChange={(e) => { setPassword(e.target.value); if (errors.password) setErrors(prev => ({ ...prev, password: undefined })); }}
                                required
                            />
                            {errors.password && (
                                <p className="text-xs text-red-500 mt-1">{errors.password}</p>
                            )}
                        </div>

                        {errors.general && (
                            <div className="text-sm text-red-500 font-medium">
                                {errors.general}
                            </div>
                        )}

                        <Button type="submit" className="w-full" disabled={loading}>
                            {loading ? 'Creating Account...' : 'Sign Up'}
                        </Button>
                    </form>
                </CardContent>
                <CardFooter className="justify-center">
                    <p className="text-sm text-gray-500">
                        Already have an account? <Link to="/login" className="text-primary hover:underline">Sign in</Link>
                    </p>
                </CardFooter>
            </Card>
        </div>
    );
}
