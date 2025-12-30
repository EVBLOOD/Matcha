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
      meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true },
      children: [
        {
          path: '',
          name: 'home',
          component: ExplorePage,
          meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Explore' },
        },
        {
          path: 'messages',
          component: MessagesPage,
          meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Chat' }
        },
        {
          path: 'notifications',
          component: NotificationsPage,
          meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Notifications' }
        },
        {
          path: 'profile',
          component: ProfilePage,
          meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: true, title: 'Profile' }
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
      meta: { requiresVerification: false, requiresAuth: true, requiresCompleteProfile: false }
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
      meta: { requiresVerification: true, requiresAuth: true, requiresCompleteProfile: false }
    }
  ],
})

router.beforeEach(async (to, from, next) => {
  const user = useUserStore();
  const token = localStorage.getItem('auth_token');

  console.log(user.isLoaded)
  console.log(token)
    if (token && !user.isLoaded) {
      await user.fetchUser();
    }
    if (!token) {
      await user.fetchUser();
      user.setIsLoaded(false)
    }

    if (user.isAuthenticated) {
      if (!user.isVerified && to.meta.requiresVerification) {
        return next({ name: 'email confirmation' });
      } else if (!user.isProfileComplete && to.meta.requiresCompleteProfile) {
        return next({ name: 'profile onboarding' });
      } else {
        if (to.meta.public) {
          return next({ name: 'home' });
        } else if (user.isVerified && !to.meta.requiresVerification) {
          return next({ name: 'profile onboarding' });
        } else if (user.isProfileComplete && !to.meta.requiresCompleteProfile) {
          return next({ name: 'home' });
        }
      }

    } else {
      if (!to.meta.public) {
          return next({ name: 'login' });
      }
    }
    next();
});
export default router
