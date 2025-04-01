// src/app/page.tsx
import ThemeInput from '@/components/ThemeInput';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-4 bg-gray-50">
      <h1 className="mb-8 text-3xl font-bold text-center text-gray-800">
        Business English Flash
      </h1>
      <div className="w-full max-w-md">
        <ThemeInput />
      </div>
    </main>
  );
}
