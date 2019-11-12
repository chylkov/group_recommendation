from vk_api import VKapi

class RecEng:
    def __init__(self, api:VKapi, embedding):
        self.api = api
        self.embedding = embedding

    def get_recommendations_from_publics(self, publics_ids, top_limit=10):
        """
        Takes VK publics and returns most relevant publics ids and scores
        :param publics_ids:list[int]
        :param top_limit: how much recommendations will be returned
        :return: list[int], list[float]
        """

        # Dummy baseline algorithm - recommend Top10 most popular VK publics without regards to input
        # Your goal - implement something more sophisticated
        #
        most_popular_publics = [27895931, 43215063, 22798006, 26419239, 45441631,
                                57846937, 58170807, 22822305, 12382740, 31836774]
        similarity = [0.1]*len(most_popular_publics)

        return most_popular_publics, similarity

    def get_recommendations_for_user(self, user_id, top_limit=10):
        user_subscriptions = self.api.get_user_subscriptions(user_id)

        if not user_subscriptions:
            return []

        publics_ids = user_subscriptions['groups']['items']
        most_similar_publics_ids, similarity = self.get_recommendations_from_publics(publics_ids, top_limit)
        # Gathering meta-information about publics using VK-API

        recommended_publics_meta = self.api.get_groups_by_id(most_similar_publics_ids)
        for meta, public_id, similarity, in zip(recommended_publics_meta, most_similar_publics_ids, similarity):
            meta['similarity'] = similarity

        return recommended_publics_meta