import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '@/views/LandingPage.vue';
import RegisterPage from '@/views/RegisterPage.vue';
import EmailConfirmationPage from '@/views/EmailConfirmationPage.vue';
import LoginPage from '@/views/LoginPage.vue';
import ProfileOnboarding from '@/views/ProfileOnboarding.vue';
import HomePage from '@/views/Protected/HomePage.vue';
import ExplorePage from '@/views/Protected/ExplorePage.vue';
import MessagesPage from '@/views/Protected/MessagesPage.vue';
import NotificationsPage from '@/views/Protected/NotificationsPage.vue';
import ProfilePage from '@/views/Protected/ProfilePage.vue';
import useUserStore from '@/stores/user';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomePage,
      children: [
        {
          path: '',
          component: ExplorePage,
          meta: { requiresAuth: true, requiresCompleteProfile: true }
        },
        {
          path: 'messages',
          component: MessagesPage,
          meta: { requiresAuth: true, requiresCompleteProfile: true }
        },
        {
          path: 'notifications',
          component: NotificationsPage,
          meta: { requiresAuth: true, requiresCompleteProfile: true }
        },
        {
          path: 'profile',
          component: ProfilePage,
          meta: { requiresAuth: true, requiresCompleteProfile: true }
        },
      ]
    },
    {
      path: '/landing',
      name: 'landing',
      component: LandingPage,
      meta: { public: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterPage,
      meta: { public: true }
    },
    {
      path: '/confirm-email', // TODO: I should find a solution to integrate this later
      name: 'email confirmation',
      component: EmailConfirmationPage,
      meta: { requiresAuth: true, requiresCompleteProfile: false }
    }, 
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
      meta: { public: true }
    },
    {
      path: '/profile-onboarding',
      name: 'profile onboarding',
      component: ProfileOnboarding,
      meta: { requiresAuth: true, requiresCompleteProfile: false }
    }
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue'),
    // },
  ],
})

router.beforeEach(async (to, from, next) => {
  const user = useUserStore();
  const token = localStorage.getItem('auth_token');


  if (to.meta.requiresAuth && (!token || !(user.isAuthenticated))) {
    return next({ name: 'login' });
  }

  if (token && !user.isLoaded) {
    await user.fetchUser();
  }

  if (user.isAuthenticated && !(user?.status === 'completed')) {
    if (to.meta.requiresCompleteProfile || !to.meta.requiresAuth) {
      return next({ name: 'profile onboarding' });
    }
  }

  if (user.isAuthenticated && (user?.status === 'completed')) {
    if (to.meta.onboarding || !to.meta.requiresAuth) {
      return next({ name: '/' });
    }
  }

  next(); 
});
export default router
