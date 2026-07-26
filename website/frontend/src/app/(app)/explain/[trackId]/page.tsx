import { ExplanationPanel } from "@/components/explainability/explanation-panel";

export default async function ExplainPage({ params }: { params: Promise<{ trackId: string }> }) {
  const { trackId } = await params;

  // In production this fetches GET /explain/{trackId} from the
  // Explainability Agent. Static narrative shown here as a structural example.
  return (
    <div className="mx-auto max-w-xl">
      <h1 className="mb-6 font-[var(--font-display)] text-2xl font-medium">Explanation</h1>
      <ExplanationPanel
        trackTitle="Golden Hour"
        narrative="You mentioned feeling calm but hopeful after a long week. This track matches your target valence closely, sits in a tempo range you've responded well to on wind-down evenings, and features an artist your taste profile weights highly."
        signals={[
          { label: "Mood match", weight: 0.86 },
          { label: "Taste affinity", weight: 0.71 },
          { label: "Novelty", weight: 0.35 },
          { label: "Arc position fit", weight: 0.62 },
        ]}
      />
      <p className="mt-3 text-xs text-[var(--color-mist-500)]">Track ID: {trackId}</p>
    </div>
  );
}
