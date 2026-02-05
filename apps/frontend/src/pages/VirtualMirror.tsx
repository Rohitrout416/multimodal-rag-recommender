import { useState } from 'react';
import api from '@/lib/api';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Upload, Sparkles, Shirt, User } from 'lucide-react';

export default function VirtualMirror() {
    const [userImage, setUserImage] = useState<string | null>(null);
    const [clothingImage, setClothingImage] = useState<string | null>(null);
    const [resultImage, setResultImage] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>, type: 'user' | 'clothing') => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                if (type === 'user') setUserImage(reader.result as string);
                else setClothingImage(reader.result as string);
            };
            reader.readAsDataURL(file);
        }
    };

    const handleGenerate = async () => {
        if (!userImage || !clothingImage) return;

        setLoading(true);
        setResultImage(null);

        try {
            // Create FormData to send specific fields if needed, 
            // but our backend TryOnRequest expects x-www-form-urlencoded compatible values or standard fields
            // Since we defined the backend to accept Form parameters:
            const formData = new FormData();
            formData.append('user_image', userImage);
            formData.append('clothing_image', clothingImage);

            const response = await api.post('/try-on', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            setResultImage(response.data.result_image_url);
        } catch (error) {
            console.error('Try-On failed:', error);
            alert('Failed to generate try-on result. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container mx-auto p-4 max-w-4xl">
            <h1 className="text-3xl font-bold mb-6 flex items-center gap-2">
                <Sparkles className="text-purple-500" /> Virtual Mirror
            </h1>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Input Section */}
                <Card className="md:col-span-1">
                    <CardHeader>
                        <CardTitle className="text-lg">Upload Images</CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium flex items-center gap-2">
                                <User size={16} /> Your Photo
                            </label>
                            <div className="border-2 border-dashed rounded-lg p-4 text-center hover:bg-accent/50 transition cursor-pointer relative h-40 flex items-center justify-center overflow-hidden">
                                <input
                                    type="file"
                                    accept="image/*"
                                    onChange={(e) => handleImageUpload(e, 'user')}
                                    className="absolute inset-0 opacity-0 cursor-pointer"
                                />
                                {userImage ? (
                                    <img src={userImage} alt="User" className="w-full h-full object-cover" />
                                ) : (
                                    <div className="text-muted-foreground">
                                        <Upload className="mx-auto mb-2" />
                                        <span className="text-xs">Click to upload</span>
                                    </div>
                                )}
                            </div>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium flex items-center gap-2">
                                <Shirt size={16} /> Garment Photo
                            </label>
                            <div className="border-2 border-dashed rounded-lg p-4 text-center hover:bg-accent/50 transition cursor-pointer relative h-40 flex items-center justify-center overflow-hidden">
                                <input
                                    type="file"
                                    accept="image/*"
                                    onChange={(e) => handleImageUpload(e, 'clothing')}
                                    className="absolute inset-0 opacity-0 cursor-pointer"
                                />
                                {clothingImage ? (
                                    <img src={clothingImage} alt="Clothing" className="w-full h-full object-cover" />
                                ) : (
                                    <div className="text-muted-foreground">
                                        <Upload className="mx-auto mb-2" />
                                        <span className="text-xs">Click to upload</span>
                                    </div>
                                )}
                            </div>
                        </div>

                        <Button
                            className="w-full"
                            onClick={handleGenerate}
                            disabled={!userImage || !clothingImage || loading}
                        >
                            {loading ? 'Processing...' : 'Try On Now'}
                        </Button>
                    </CardContent>
                </Card>

                {/* Result Section */}
                <Card className="md:col-span-2 flex flex-col">
                    <CardHeader>
                        <CardTitle className="text-lg">Result</CardTitle>
                    </CardHeader>
                    <CardContent className="flex-1 flex items-center justify-center bg-muted/20 min-h-[400px]">
                        {loading ? (
                            <div className="text-center animate-pulse">
                                <Sparkles className="h-12 w-12 mx-auto text-purple-500 mb-4" />
                                <p className="text-lg font-medium">Magic is happening...</p>
                                <p className="text-sm text-muted-foreground">This may take a few seconds</p>
                            </div>
                        ) : resultImage ? (
                            <img src={resultImage} alt="Try-On Result" className="max-w-full max-h-[500px] rounded-lg shadow-lg" />
                        ) : (
                            <div className="text-center text-muted-foreground">
                                <p>Upload images and click "Try On Now" to see the magic.</p>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
