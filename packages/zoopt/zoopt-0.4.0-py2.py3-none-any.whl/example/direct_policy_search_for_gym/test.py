def sum_reward(self, solution):
    """
    Objective function of racos by summation of reward in a trajectory

    :param solution: a data structure containing x and fx
    :return: value of fx
    """
    x = solution.get_x()
    sum_re = 0
    # reset stop step
    self.__stop_step = self.__max_step
    # reset nn model weight
    self.__policy_model.decode_w(x)
    # reset environment
    observation = self.__envir.reset()
    for i in range(self.__max_step):
        action = self.nn_policy_sample(observation)
        observation, reward, done, info = self.__envir.step(action)
        sum_re += reward
        if done:
            self.__stop_step = i
            break
        self.total_step += 1
    value = sum_re
    name = self.__envir_name
    # turn the direction for minimization
    if name == 'CartPole-v0' or name == 'CartPole-v1' or name == 'MountainCar-v0' or name == 'Acrobot-v1' or name == 'HalfCheetah-v1' \
            or name == 'Humanoid-v1' or name == 'Swimmer-v1' or name == 'Ant-v1' or name == 'Hopper-v1' \
            or name == 'LunarLander-v2' or name == 'BipedalWalker-v2':
        value = -value
    return value