// src/app/progress/page.tsx
import Progress from '@/components/Progress';

export default function ProgressPage() {
  return (
    <main className="min-h-screen p-4 bg-gray-50">
      <div className="max-w-md mx-auto">
        <h1 className="text-3xl font-bold mb-6 text-center text-gray-800">
          Business English Flash
        </h1>
        <Progress />
      </div>
    </main>
  );
}
