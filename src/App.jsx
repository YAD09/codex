import Hero from './components/Hero.jsx';
import Story from './components/Story.jsx';
import Pipeline from './components/Pipeline.jsx';
import Analytics from './components/Analytics.jsx';
import TechStack from './components/TechStack.jsx';
import CTA from './components/CTA.jsx';

const App = () => (
  <div className="relative bg-midnight">
    <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_70%_20%,_rgba(124,58,237,0.18),_transparent_45%)] opacity-70" />
    <Hero />
    <Story />
    <Pipeline />
    <Analytics />
    <TechStack />
    <CTA />
  </div>
);

export default App;
