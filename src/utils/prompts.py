BRAND_PROFILE_PROMPT = """
You are an expert brand strategist. Your task is to extract a comprehensive brand profile from the provided website content.
Focus on identifying the core identity, what they do, who they serve, and what they stand for.

Input Website Content:
{content}

Extract and generate the following fields:
1. brand_name: The name of the brand.
2. industry: The primary industry or market category.
3. mission: The brand's mission statement or core purpose.
4. description: A clear, concise description of the company.
5. products: A list of key products, services, or features offered.
"""

CREATOR_GUIDELINES_PROMPT = """
You are an expert brand manager and influencer marketer. Your task is to generate practical, creator-focused guidelines based on the provided Brand Profile.
These guidelines will be used by content creators (influencers, UGC creators) to produce authentic content that aligns with the brand's identity.

Brand Profile:
{brand_profile}

Generate the following fields:
1. tone_of_voice: Describe the brand's tone of voice (e.g., "Playful and energetic", "Professional and trustworthy").
2. dos: A list of practical "Do's" for creators (e.g., "Do show the product in natural lighting", "Do use casual, everyday language").
3. donts: A list of practical "Don'ts" for creators (e.g., "Don't mention competitors", "Don't use overly scripted or formal language").
4. content_suggestions: A list of creative content ideas or hooks that would work well for this brand.

Ensure the guidelines are actionable, specific, and avoid generic marketing fluff.
"""

COMPETITOR_DISCOVERY_PROMPT = """
You are an expert market analyst. Based on the provided Brand Profile, infer 3-5 top competitors in the market.
Base your inference on the industry, products, services, target audience, and market positioning.

Brand Profile:
{brand_profile}

For each competitor, provide:
1. name: The competitor's name.
2. industry: Their primary industry.
3. reasoning: Why they are considered a competitor to the original brand.
4. relevance_score: An integer score from 1-100 indicating how close of a competitor they are.
"""

COMPETITOR_INTELLIGENCE_PROMPT = """
You are a competitive intelligence strategist. Generate a realistic and accurate Competitor Profile for the given competitor name.
Consider their known market presence, target audience, and typical marketing strategies.

Competitor Name: {competitor_name}
Competitor Industry/Context: {competitor_context}

Provide:
1. company_name: Name of the company.
2. positioning_summary: A brief summary of how they position themselves in the market.
3. strengths: A list of their key strengths.
4. target_audience: Who they primarily target.
5. content_strategy_summary: A summary of their typical social media and content marketing approach.
"""

SOCIAL_SIMULATION_PROMPT = """
You are an expert social media manager. Your task is to simulate realistic social media posts for the given profile.
You MUST generate between 10 and 15 posts. 
The posts should reflect the brand's industry, audience, and product category. Do not generate random posts.
Make the engagement metrics (likes, comments, shares) realistic for the brand's size.

Profile Data (Brand or Competitor):
{profile_data}

For each post, provide:
1. caption: The post caption.
2. image_description: A description of the visual content.
3. likes: Integer.
4. comments: Integer.
5. shares: Integer.
6. post_date: A realistic date string (e.g., '2023-10-15').
7. content_type: The type of post (e.g., Educational, Promotional, Founder Story, Product Showcase, Customer Success, Industry Insight).
"""

GAP_ANALYSIS_PROMPT = """
You are a top-tier marketing consultant. Perform a Competitive Gap Analysis.
Analyze the differences between the original Brand and its Competitors, using the provided intelligence profiles and engagement metrics.

Data:
Brand Profile:
{brand_profile}

Engagement Metrics:
{metrics}

Competitor Profiles:
{competitor_profiles}

Output the analysis focusing on:
1. content_gaps: Gaps in content strategy.
2. positioning_gaps: Gaps in market positioning.
3. branding_gaps: Differences in branding approaches.
4. engagement_gaps: Differences in engagement performance.
5. opportunity_areas: Specific, actionable areas where the brand can outperform competitors.

Use evidence-based statements referencing the metrics and profiles (e.g., "Competitors publish educational content 45% of the time while the brand publishes only 8%"). Avoid generic fluff.
"""

GROWTH_STRATEGY_PROMPT = """
You are a strategic growth hacker. Based on the entire intelligence package (Brand, Gap Analysis, Competitors, Analytics), generate a highly actionable Social Growth Strategy for the brand.

Context Data:
{context_data}

Generate:
1. quick_wins: Easy-to-implement actions for immediate impact.
2. medium_term_improvements: Structural changes to strategy.
3. long_term_recommendations: Strategic overhauls.
4. content_ideas: Specific, creative content concepts.
5. posting_strategy_suggestions: Frequency, timing, and platform focus.

Ensure recommendations directly address the gaps found in the Gap Analysis and exploit competitor weaknesses.
"""
