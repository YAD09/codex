import { motion } from 'framer-motion';
import { fadeIn, slideUp, staggerChildren } from '../motion/variants';

const cards = [
  {
    title: 'Problem',
    text: 'Offline stores lack measurable analytics.',
    accent: 'from-rose-500/30 to-transparent',
    align: 'justify-self-start',
  },
  {
    title: 'Solution',
    text: 'AI analyzes CCTV footage in real time.',
    accent: 'from-cyan-400/30 to-transparent',
    align: 'justify-self-end',
  },
];

const Story = () => (
  <section className="section-padding bg-black">
    <motion.div
      className="mx-auto grid max-w-5xl gap-10"
      variants={staggerChildren}
      initial="hidden"
      whileInView="visible"
      viewport={{ once: true, amount: 0.3 }}
    >
      <motion.p
        className="text-sm uppercase tracking-[0.4em] text-slate-400"
        variants={fadeIn}
      >
        Problem → Solution
      </motion.p>
      <div className="grid gap-8 md:grid-cols-2">
        {cards.map((card) => (
          <motion.div
            key={card.title}
            className={`card-glass ${card.align} group relative overflow-hidden rounded-3xl px-8 py-10`}
            variants={slideUp}
          >
            <div
              className={`absolute inset-0 bg-gradient-to-br ${card.accent} opacity-0 transition-opacity duration-500 group-hover:opacity-100`}
            />
            <div className="relative z-10">
              <h3 className="text-2xl font-semibold text-white">{card.title}</h3>
              <p className="mt-4 text-lg text-slate-300">{card.text}</p>
            </div>
          </motion.div>
        ))}
      </div>
    </motion.div>
  </section>
);

export default Story;
