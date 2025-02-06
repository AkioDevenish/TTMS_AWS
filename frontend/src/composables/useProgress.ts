import NProgress from 'nprogress';
import 'nprogress/nprogress.css';

NProgress.configure({ showSpinner: true });

export function useProgress() {
  const start = () => NProgress.start();
  const done = () => NProgress.done();

  return { start, done };
}