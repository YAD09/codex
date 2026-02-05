import { motion } from 'framer-motion';
import { fadeIn, slideUp, staggerChildren, hoverGlow } from '../motion/variants';

const metrics = [
  { label: 'Daily Footfall', value: '12.4K' },
  { label: 'Avg. Dwell', value: '4m 12s' },
  { label: 'Hotspot Density', value: '86%' },
];

const Analytics = () => (
  <section className="section-padding bg-black">
    <motion.div
      className="mx-auto max-w-6xl"
      variants={staggerChildren}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.3 }}
    >
      <motion.div className="mb-10" variants={fadeIn}>
        <p className="text-sm uppercase tracking-[0.4em] text-slate-400">Analytics</p>
        <h2 className="mt-4 text-3xl font-semibold text-white md:text-4xl">
          Heatmap Intelligence
        </h2>
      </motion.div>
      <div className="grid gap-8 lg:grid-cols-[2fr_1fr]">
        <motion.div
          className="relative overflow-hidden rounded-3xl border border-white/10 bg-gradient-to-br from-[#0b1220] via-[#111827] to-[#020617] p-10"
          variants={slideUp}
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(59,130,246,0.15),_transparent_55%)]" />
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_70%,_rgba(239,68,68,0.25),_transparent_50%)]" />
          <div className="relative z-10 h-72 rounded-2xl border border-white/10 bg-gradient-to-br from-blue-500/10 via-slate-900 to-red-500/10">
            <div className="absolute inset-0 opacity-80 mix-blend-screen">
              <div className="absolute left-12 top-10 h-32 w-32 rounded-full bg-blue-500/40 blur-3xl" />
              <div className="absolute right-10 top-20 h-36 w-36 rounded-full bg-red-500/40 blur-3xl" />
              <div className="absolute bottom-8 left-1/2 h-28 w-28 -translate-x-1/2 rounded-full bg-amber-400/40 blur-3xl" />
            </div>
            <div className="absolute inset-0 bg-[linear-gradient(90deg,_rgba(255,255,255,0.04)_1px,_transparent_1px),_linear-gradient(180deg,_rgba(255,255,255,0.04)_1px,_transparent_1px)] [background-size:48px_48px]" />
            <motion.div
              className="absolute left-0 right-0 top-0 h-12 bg-gradient-to-r from-transparent via-neon/30 to-transparent"
              animate={{ y: [0, 220, 0] }}
              transition={{ duration: 6, repeat: Infinity, ease: 'easeInOut' }}
            />
          </div>
        </motion.div>
        <div className="grid gap-6">
          {metrics.map((metric) => (
            <motion.div
              key={metric.label}
              className="card-glass rounded-2xl px-6 py-6"
              variants={slideUp}
              initial="rest"
              whileHover="hover"
              animate="rest"
            >
              <motion.div variants={hoverGlow}>
                <p className="text-sm uppercase tracking-[0.3em] text-slate-400">
                  {metric.label}
                </p>
                <p className="mt-4 text-3xl font-semibold text-white">
                  {metric.value}
                </p>
              </motion.div>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  </section>
);

export default Analytics;
