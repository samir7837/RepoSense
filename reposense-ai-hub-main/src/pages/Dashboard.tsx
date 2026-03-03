import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { dashboardApi } from "@/services/api";
import DashboardSidebar from "@/components/DashboardSidebar";
import { FolderGit2, FileSearch, Star, ChevronRight } from "lucide-react";
import { motion } from "framer-motion";

interface Repo {
  repo_name: string;
  full_name: string;
  total_reviews: number;
  average_score: number;
}

interface Review {
  repo_name: string;
  file_name: string;
  score: number;
  review: string;
  created_at: string;
}

export default function Dashboard() {
  const { githubId, login } = useAuth();
  const [repos, setRepos] = useState<Repo[]>([]);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [selectedRepo, setSelectedRepo] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!githubId) return;

    Promise.all([
      dashboardApi.getRepos(githubId),
      dashboardApi.getReviews(githubId),
    ])
      .then(([reposRes, reviewsRes]) => {
        setRepos(reposRes.data || []);
        setReviews(reviewsRes.data || []);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [githubId]);

  const avgScore = reviews.length
    ? (
        reviews.reduce((a, r) => a + (r.score || 0), 0) / reviews.length
      ).toFixed(1)
    : "—";

  const filteredReviews = selectedRepo
    ? reviews.filter((r) => r.repo_name === selectedRepo)
    : reviews;

  const stats = [
    {
      label: "Total Repositories",
      value: repos.length,
      icon: FolderGit2,
      color: "text-gradient-purple",
    },
    {
      label: "Total Reviews",
      value: reviews.length,
      icon: FileSearch,
      color: "text-gradient-pink",
    },
    {
      label: "Average Score",
      value: avgScore,
      icon: Star,
      color: "text-gradient-blue",
    },
  ];

  return (
    <div className="flex h-screen bg-background">
      <DashboardSidebar />

      <main className="flex-1 overflow-auto">
        <div className="p-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-2xl font-bold">Dashboard</h1>
            <p className="text-sm text-muted-foreground mt-1">
              Welcome back{login ? `, ${login}` : ""}
            </p>
          </div>

          {/* Stats */}
          <div className="grid gap-6 sm:grid-cols-3 mb-8">
            {stats.map((s, i) => (
              <motion.div
                key={s.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="stat-card-gradient rounded-xl p-6"
              >
                <div className="flex items-center justify-between mb-3">
                  <span className="text-sm text-muted-foreground">
                    {s.label}
                  </span>
                  <s.icon className={`h-5 w-5 ${s.color}`} />
                </div>
                <p className="text-3xl font-bold">
                  {loading ? "..." : s.value}
                </p>
              </motion.div>
            ))}
          </div>

          {/* Repositories Table */}
          <div className="glass-card rounded-xl overflow-hidden mb-8">
            <div className="flex items-center justify-between p-5 border-b border-border">
              <h2 className="font-semibold">Repositories</h2>
              {selectedRepo && (
                <button
                  onClick={() => setSelectedRepo(null)}
                  className="text-xs text-primary hover:underline"
                >
                  Clear filter
                </button>
              )}
            </div>

            {loading ? (
              <div className="p-8 text-center text-muted-foreground">
                Loading...
              </div>
            ) : repos.length === 0 ? (
              <div className="p-8 text-center text-muted-foreground">
                No repositories found. Push code to get started.
              </div>
            ) : (
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border text-muted-foreground">
                    <th className="text-left p-4 font-medium">Repo Name</th>
                    <th className="text-left p-4 font-medium">
                      Files Reviewed
                    </th>
                    <th className="text-left p-4 font-medium">Avg Score</th>
                    <th className="p-4" />
                  </tr>
                </thead>
                <tbody>
                  {repos.map((repo) => (
                    <tr
                      key={repo.repo_name}
                      className="border-b border-border/50 hover:bg-secondary/30 cursor-pointer transition-colors"
                      onClick={() => setSelectedRepo(repo.repo_name)}
                    >
                      <td className="p-4 font-medium">
                        {repo.repo_name}
                      </td>
                      <td className="p-4 text-muted-foreground">
                        {repo.total_reviews}
                      </td>
                      <td className="p-4">
                        <span className="gradient-text font-semibold">
                          {repo.average_score ?? "—"}
                        </span>
                      </td>
                      <td className="p-4">
                        <ChevronRight className="h-4 w-4 text-muted-foreground" />
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {/* Reviews Table */}
          <div className="glass-card rounded-xl overflow-hidden">
            <div className="p-5 border-b border-border">
              <h2 className="font-semibold">
                {selectedRepo
                  ? `Reviews — ${selectedRepo}`
                  : "All Reviews"}
              </h2>
            </div>

            {loading ? (
              <div className="p-8 text-center text-muted-foreground">
                Loading...
              </div>
            ) : filteredReviews.length === 0 ? (
              <div className="p-8 text-center text-muted-foreground">
                No reviews yet.
              </div>
            ) : (
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border text-muted-foreground">
                    <th className="text-left p-4 font-medium">
                      File Name
                    </th>
                    <th className="text-left p-4 font-medium">
                      Score
                    </th>
                    <th className="text-left p-4 font-medium">
                      Review
                    </th>
                    <th className="text-left p-4 font-medium">
                      Date
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filteredReviews.map((r, i) => (
                    <tr
                      key={i}
                      className="border-b border-border/50 hover:bg-secondary/30 transition-colors"
                    >
                      <td className="p-4 font-medium">
                        {r.file_name}
                      </td>
                      <td className="p-4">
                        <span
                          className={`font-semibold ${
                            r.score >= 70
                              ? "text-green-400"
                              : r.score >= 40
                              ? "text-yellow-400"
                              : "text-red-400"
                          }`}
                        >
                          {r.score}/100
                        </span>
                      </td>
                      <td className="p-4 text-muted-foreground max-w-xs truncate">
                        {r.review}
                      </td>
                      <td className="p-4 text-muted-foreground">
                        -
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}