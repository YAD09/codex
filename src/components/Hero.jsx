import { useEffect } from 'react';
import { motion, useMotionValue, useTransform } from 'framer-motion';
import { fadeIn, slideUp, staggerChildren } from '../motion/variants';

const Hero = () => {
  const mouseX = useMotionValue(0);
  const mouseY = useMotionValue(0);

  useEffect(() => {
    const handleMove = (event) => {
      const { innerWidth, innerHeight } = window;
      mouseX.set((event.clientX - innerWidth / 2) / innerWidth);
      mouseY.set((event.clientY - innerHeight / 2) / innerHeight);
    };
    window.addEventListener('mousemove', handleMove);
    return () => window.removeEventListener('mousemove', handleMove);
  }, [mouseX, mouseY]);

  const translateX = useTransform(mouseX, [-0.5, 0.5], [-30, 30]);
  const translateY = useTransform(mouseY, [-0.5, 0.5], [-20, 20]);

  return (
    <section className="relative min-h-screen overflow-hidden bg-midnight">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(64,243,255,0.18),_transparent_60%)]" />
      <div className="absolute inset-0 opacity-40 bg-grid [background-size:48px_48px]" />
      <motion.div
        className="absolute -top-32 right-10 h-72 w-72 rounded-full bg-pulse/40 blur-[120px]"
        style={{ x: translateX, y: translateY }}
        animate={{ scale: [1, 1.1, 1], opacity: [0.4, 0.7, 0.4] }}
        transition={{ duration: 12, repeat: Infinity, ease: 'easeInOut' }}
      />
      <motion.div
        className="absolute bottom-10 left-0 h-80 w-80 rounded-full bg-ember/30 blur-[140px]"
        style={{ x: translateX, y: translateY }}
        animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0.6, 0.3] }}
        transition={{ duration: 10, repeat: Infinity, ease: 'easeInOut' }}
      />

      <div className="section-padding relative z-10 flex min-h-screen items-center">
        <motion.div
          className="max-w-3xl"
          variants={staggerChildren}
          initial="hidden"
          animate="visible"
        >
          <motion.p
            className="mb-6 inline-flex items-center gap-3 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.3em] text-neon"
            variants={fadeIn}
          >
            Retail Vision Lab
            <span className="h-2 w-2 rounded-full bg-neon shadow-glow" />
          </motion.p>
          <motion.h1
            className="text-balance text-4xl font-semibold text-white md:text-6xl lg:text-7xl"
            variants={slideUp}
          >
            AI-Powered Retail Intelligence
          </motion.h1>
          <motion.p
            className="mt-6 text-lg text-slate-300 md:text-xl"
            variants={slideUp}
          >
            People Counting &amp; Heatmaps using Computer Vision
          </motion.p>
          <motion.div
            className="mt-10 flex flex-wrap items-center gap-6"
            variants={slideUp}
          >
            <div className="card-glass rounded-2xl px-6 py-4">
              <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Latency</p>
              <p className="mt-2 text-2xl font-semibold text-white">120ms</p>
            </div>
            <div className="card-glass rounded-2xl px-6 py-4">
              <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Accuracy</p>
              <p className="mt-2 text-2xl font-semibold text-white">98.7%</p>
            </div>
          </motion.div>
        </motion.div>
      </div>
    </section>
  );
};

export default Hero;
