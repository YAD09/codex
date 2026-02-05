import { motion } from 'framer-motion';
import { fadeIn, slideUp, staggerChildren } from '../motion/variants';

const steps = [
  'CCTV Input',
  'YOLOv8 Detection',
  'DeepSORT Tracking',
  'People Counting',
  'Heatmap Generation',
];

const Pipeline = () => (
  <section className="section-padding bg-midnight">
    <motion.div
      className="mx-auto max-w-6xl"
      variants={staggerChildren}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.3 }}
    >
      <motion.div className="mb-12" variants={fadeIn}>
        <p className="text-sm uppercase tracking-[0.4em] text-slate-400">
          AI Pipeline
        </p>
        <h2 className="mt-4 text-3xl font-semibold text-white md:text-4xl">
          Signal to Insight
        </h2>
      </motion.div>
      <div className="grid gap-6 md:grid-cols-5">
        {steps.map((step, index) => (
          <motion.div
            key={step}
            className="relative"
            variants={slideUp}
          >
            <div className="card-glass flex h-full flex-col justify-between rounded-2xl px-5 py-6">
              <span className="text-xs uppercase tracking-[0.3em] text-slate-400">
                Step {index + 1}
              </span>
              <p className="mt-6 text-lg font-medium text-white">{step}</p>
            </div>
            {index < steps.length - 1 && (
              <motion.div
                className="absolute -right-3 top-1/2 hidden h-0.5 w-6 bg-gradient-to-r from-neon to-transparent md:block"
                initial={{ scaleX: 0 }}
                whileInView={{ scaleX: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                style={{ originX: 0 }}
              />
            )}
          </motion.div>
        ))}
      </div>
    </motion.div>
  </section>
);

export default Pipeline;
