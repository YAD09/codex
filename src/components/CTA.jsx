import { motion } from 'framer-motion';
import { fadeIn, slideUp } from '../motion/variants';

const CTA = () => (
  <section className="section-padding bg-black">
    <motion.div
      className="mx-auto flex max-w-4xl flex-col items-start gap-8 rounded-3xl border border-white/10 bg-gradient-to-br from-white/5 via-white/5 to-neon/10 p-12"
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.3 }}
      variants={fadeIn}
    >
      <motion.p
        className="text-sm uppercase tracking-[0.4em] text-slate-400"
        variants={slideUp}
      >
        24-Hour Hackathon Prototype
      </motion.p>
      <motion.h2
        className="text-3xl font-semibold text-white md:text-4xl"
        variants={slideUp}
      >
        Real-Time Retail Intelligence
      </motion.h2>
      <motion.button
        className="group relative overflow-hidden rounded-full border border-neon/40 px-8 py-3 text-sm uppercase tracking-[0.4em] text-neon"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.98 }}
        variants={slideUp}
      >
        <span className="absolute inset-0 bg-neon/20 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
        <span className="relative z-10">View Demo</span>
      </motion.button>
    </motion.div>
  </section>
);

export default CTA;
