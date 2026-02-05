import { motion } from 'framer-motion';
import { slideUp, staggerChildren, hoverGlow } from '../motion/variants';

const stack = ['Python', 'YOLOv8', 'DeepSORT', 'OpenCV', 'PyTorch'];

const TechStack = () => (
  <section className="section-padding bg-midnight">
    <motion.div
      className="mx-auto max-w-6xl"
      variants={staggerChildren}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.3 }}
    >
      <motion.div className="mb-10" variants={slideUp}>
        <p className="text-sm uppercase tracking-[0.4em] text-slate-400">Tech Stack</p>
        <h2 className="mt-4 text-3xl font-semibold text-white md:text-4xl">
          Built for Real-Time Vision
        </h2>
      </motion.div>
      <div className="grid gap-6 md:grid-cols-3">
        {stack.map((item) => (
          <motion.div
            key={item}
            className="group card-glass rounded-2xl px-6 py-8 text-center"
            variants={slideUp}
            whileHover={{ y: -6 }}
            transition={{ duration: 0.3 }}
          >
            <motion.div variants={hoverGlow} initial="rest" whileHover="hover" animate="rest">
              <div className="mx-auto mb-4 h-12 w-12 rounded-full border border-neon/40 bg-neon/10 shadow-glow transition-all duration-300 group-hover:scale-110" />
              <p className="text-lg font-medium text-white">{item}</p>
              <p className="mt-2 text-sm text-slate-400">Optimized pipeline component</p>
            </motion.div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  </section>
);

export default TechStack;
