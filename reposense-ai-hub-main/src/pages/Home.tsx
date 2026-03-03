import { motion } from "framer-motion";
import { Github, Bot, FileText, GitBranch, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import Navbar from "@/components/Navbar";
import { authApi } from "@/services/api";

const features = [
  {
    icon: Bot,
    title: "AI Code Review",
    description: "Get intelligent, context-aware code reviews powered by advanced AI models.",
  },
  {
    icon: FileText,
    title: "AI README Improver",
    description: "Automatically enhance your README files with better structure and documentation.",
  },
  {
    icon: GitBranch,
    title: "GitHub Integration",
    description: "Seamlessly connects with your GitHub repositories via webhooks.",
  },
  {
    icon: Zap,
    title: "Real-time Analysis",
    description: "Instant analysis on every push with detailed scoring and feedback.",
  },
];

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
};

const itemVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      {/* Hero */}
      <section className="relative flex min-h-screen items-center justify-center overflow-hidden hero-gradient pt-16">
        {/* Ambient orbs */}
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute left-1/4 top-1/4 h-96 w-96 rounded-full bg-gradient-purple/10 blur-[120px] animate-pulse-glow" />
          <div className="absolute right-1/4 top-1/3 h-80 w-80 rounded-full bg-gradient-pink/8 blur-[100px] animate-pulse-glow" style={{ animationDelay: "1s" }} />
          <div className="absolute bottom-1/4 left-1/2 h-72 w-72 rounded-full bg-gradient-blue/10 blur-[100px] animate-pulse-glow" style={{ animationDelay: "2s" }} />
        </div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="relative z-10 text-center px-6"
        >
          <h1 className="text-6xl font-black tracking-tight sm:text-8xl mb-6">
            <span className="gradient-text">RepoSense</span>
          </h1>
          <p className="mx-auto max-w-xl text-lg text-muted-foreground mb-10">
            AI-Powered GitHub Code Reviewer & README Improver
          </p>
          <a href={authApi.loginUrl}>
            <Button size="lg" className="gap-3 px-8 py-6 text-base font-semibold bg-primary hover:bg-primary/90 glow-purple">
              <Github className="h-5 w-5" />
              Login with GitHub
            </Button>
          </a>
        </motion.div>
      </section>

      {/* Features */}
      <section className="relative py-32 px-6">
        <div className="container mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-3xl font-bold mb-4 sm:text-4xl">
              What's in it for you?
            </h2>
            <p className="text-muted-foreground max-w-md mx-auto">
              Everything you need to level up your code quality and documentation.
            </p>
          </motion.div>

          <motion.div
            variants={containerVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4"
          >
            {features.map((f) => (
              <motion.div
                key={f.title}
                variants={itemVariants}
                className="glass-card rounded-xl p-6 hover:border-primary/30 transition-colors group"
              >
                <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary/10 text-primary group-hover:bg-primary/20 transition-colors">
                  <f.icon className="h-6 w-6" />
                </div>
                <h3 className="text-lg font-semibold mb-2">{f.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{f.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border/50 py-8 text-center text-sm text-muted-foreground">
        RepoSense © 2026
      </footer>
    </div>
  );
}
