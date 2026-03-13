-- MySQL dump 10.13  Distrib 5.7.12, for Win64 (x86_64)
--
-- Host: localhost    Database: kisansathi
-- ------------------------------------------------------
-- Server version	5.5.52-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ai_verification`
--

DROP TABLE IF EXISTS `ai_verification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ai_verification` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `expert_name` varchar(100) DEFAULT NULL,
  `disease` varchar(200) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `correction` text,
  `verify_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ai_verification`
--

LOCK TABLES `ai_verification` WRITE;
/*!40000 ALTER TABLE `ai_verification` DISABLE KEYS */;
INSERT INTO `ai_verification` VALUES (1,'Anil Reddy','Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot','Correct','','2026-02-19 19:33:28');
/*!40000 ALTER TABLE `ai_verification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chatbot_knowledge`
--

DROP TABLE IF EXISTS `chatbot_knowledge`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `chatbot_knowledge` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywords` text,
  `question` text,
  `response` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chatbot_knowledge`
--

LOCK TABLES `chatbot_knowledge` WRITE;
/*!40000 ALTER TABLE `chatbot_knowledge` DISABLE KEYS */;
INSERT INTO `chatbot_knowledge` VALUES (1,'rice yield, rice cultivation, grow rice, rice farming','How should I grow rice for better yield?','To grow rice with better yield, proper land preparation, seed selection, and water management are very important. Start by preparing the field with good leveling to ensure uniform water distribution. Use certified high-yielding rice seeds suitable for your region. Maintain adequate water during the vegetative stage but avoid excessive flooding. Apply fertilizers based on soil test results, especially nitrogen, phosphorus, and potassium in recommended quantities. Regular monitoring for pests and diseases and timely control measures can significantly improve rice yield.'),(2,'rice leaves yellow, yellow leaves rice, nitrogen deficiency rice','Why are my rice leaves turning yellow?','Yellowing of rice leaves can occur due to nutrient deficiency, especially nitrogen deficiency, water stress, or pest infestation. Poor drainage and over-irrigation can also cause yellowing. Check soil fertility and apply nitrogen fertilizer in split doses. If pests or diseases are present, identify them early and apply suitable control measures. Maintaining proper irrigation and balanced fertilization helps prevent leaf yellowing.'),(3,'rice fertilizer, best fertilizer rice, urea dap potash rice','What fertilizer is best for rice cultivation?','Rice requires a balanced supply of nutrients. Commonly used fertilizers include urea for nitrogen, DAP for phosphorus, and potash for potassium. The exact quantity depends on soil fertility, crop stage, and local recommendations. Applying fertilizers in split doses rather than all at once improves nutrient absorption and reduces wastage. Organic manure can also be added to improve soil health.'),(4,'rice water requirement, irrigation rice, water for rice','How much water does rice need?','Rice generally needs standing water during most of its growth period, especially during transplanting and tillering stages. However, continuous flooding is not always necessary. Alternate wetting and drying methods can save water and improve root growth. Proper water management reduces disease occurrence and improves yield.'),(5,'crop disease identification, plant disease detection, leaf disease','How can I identify crop diseases early?','Early identification of crop diseases involves regular observation of crop leaves, stems, and roots. Look for signs such as spots, discoloration, wilting, or unusual growth. Using AI-based crop disease detection tools, farmers can upload images of affected plants and receive instant disease identification and guidance. Early detection helps reduce crop loss.'),(6,'pest attack crop, pest control farming, insects crops','What should I do if pests attack my crop?','If pests attack your crop, first identify the type of pest. Avoid excessive pesticide use without proper identification. Use integrated pest management practices such as crop rotation, biological control, and recommended pesticides. Applying pesticides only when necessary reduces cost and environmental damage.'),(7,'increase crop yield, natural farming, organic yield','How can I increase crop yield naturally?','Crop yield can be increased naturally by maintaining soil fertility through organic manure, crop rotation, and proper irrigation practices. Using quality seeds, timely sowing, and controlling weeds also help. Balanced fertilizer use and early disease detection contribute to higher productivity.'),(8,'soil fertility decrease, soil health problem','Why is my soil becoming less fertile every year?','Soil fertility decreases due to continuous cropping, excessive fertilizer use, poor organic matter content, and improper irrigation. Adding organic manure, green manure crops, and reducing chemical fertilizer overuse can restore soil fertility. Soil testing helps in applying the right nutrients.'),(9,'fertilizer timing, when to apply fertilizer','When is the right time to apply fertilizer?','Fertilizers should be applied based on crop growth stage. Applying fertilizer during early growth promotes strong plant development. Split application of nitrogen fertilizer reduces nutrient loss and improves crop absorption. Avoid applying fertilizers before heavy rainfall.'),(10,'crop nutrient deficiency, fertilizer need crop','How can I know if my crop needs fertilizer?','Signs such as slow growth, pale leaves, and reduced tillering indicate nutrient deficiency. Soil testing provides accurate information about nutrient levels. AI-based fertilizer recommendation systems can also suggest fertilizer requirements based on soil and crop data.'),(11,'crop not growing, poor crop growth','Why are my crop plants not growing properly even after using fertilizer?','Poor crop growth even after fertilizer use can happen due to improper fertilizer type, wrong dosage, or poor soil health. Overuse of fertilizers can damage roots and reduce nutrient absorption. Soil pH imbalance, water stress, or disease can also affect growth. It is recommended to conduct a soil test and apply fertilizers as per crop stage and requirement. Maintaining proper irrigation and drainage is equally important.'),(12,'crop infection flowering stage','What should I do if my crop gets infected during the flowering stage?','The flowering stage is very sensitive for crops. If infection occurs during this stage, avoid excessive pesticide application. Identify the disease correctly and use recommended control measures. Maintaining proper moisture and nutrition helps the crop recover. Early expert guidance and timely treatment can reduce yield loss.'),(13,'reduce pesticide use, natural pest control','How can I prevent pests without using too many chemicals?','Pest control can be managed by following integrated pest management practices. These include crop rotation, using pest-resistant varieties, removing infected plant parts, and encouraging natural predators. Chemical pesticides should be used only when necessary and in recommended doses to avoid resistance and environmental damage.'),(14,'crop harvest time, when to harvest crop','How do I know if my crop is ready for harvesting?','Crops are ready for harvest when they reach physiological maturity. Common signs include change in crop color, drying of leaves, hardening of grains, and reduction in moisture content. Harvesting at the right time improves grain quality and market value. Local crop guidelines can help determine the ideal harvest time.'),(15,'low crop yield, poor harvest','Why is my crop yield lower than expected?','Low crop yield can result from poor seed quality, nutrient deficiency, improper irrigation, pest attack, or unfavorable weather conditions. Incorrect sowing time and spacing also affect yield. Regular monitoring, timely management practices, and following expert recommendations can help improve productivity.'),(16,'soil testing importance','How important is soil testing before planting a crop?','Soil testing helps determine nutrient levels, soil pH, and organic matter content. It allows farmers to apply the right type and quantity of fertilizers, avoiding unnecessary expenses. Soil testing improves crop health, yield, and long-term soil fertility.'),(17,'crop variety selection, high yielding varieties','Can changing crop varieties improve my income?','Yes, choosing high-yielding and disease-resistant crop varieties suited to local climate conditions can significantly improve productivity and income. Improved varieties require less pesticide usage and offer better market value. Consulting experts before selecting crop varieties is recommended.'),(18,'extreme weather crop damage','Why does my crop suffer during extreme weather conditions?','Extreme weather such as heavy rainfall, drought, or high temperatures causes stress to crops, affecting growth and yield. Waterlogging, heat stress, and moisture deficiency damage plant tissues. Adopting proper irrigation practices, mulching, and weather-resilient crop varieties can reduce damage.'),(19,'reduce farming cost','How can I reduce farming costs without reducing yield?','Farming costs can be reduced by using fertilizers efficiently, avoiding unnecessary pesticide applications, using organic manure, and adopting modern farming techniques. Group discussions with other farmers and expert guidance help in identifying cost-effective practices.'),(20,'farmer collaboration, farmer groups','How can I learn from other farmers growing the same crop?','Joining farmer collaboration groups allows farmers growing similar crops to share experiences, discuss problems, and learn successful practices. Peer learning helps avoid common mistakes and improves confidence. Expert moderation ensures reliable information sharing.'),(21,'leaf edge drying potassium deficiency','Why are my crop leaves drying from the edges?','Drying of leaf edges usually occurs due to potassium deficiency, water stress, or excessive fertilizer use. Poor irrigation practices and high temperatures can also cause this problem. Applying balanced fertilizers, maintaining proper soil moisture, and avoiding excess chemicals can help prevent leaf edge drying.'),(22,'crop irrigation schedule','How often should I irrigate my crop?','Irrigation frequency depends on crop type, soil condition, and weather. Sandy soils need frequent irrigation, while clay soils retain moisture longer. Over-irrigation can damage roots and cause diseases, while under-irrigation leads to stress. Following crop-specific irrigation schedules improves growth and yield.'),(23,'weed control farming','What should I do if weeds are growing heavily in my field?','Weeds compete with crops for nutrients, water, and sunlight. Early weed removal is important to protect crop growth. Manual weeding, mulching, and recommended herbicides can be used depending on crop stage. Timely weed control reduces yield loss.'),(24,'flower drop fruit set problem','Why are flowers falling before fruit formation?','Flower drop can occur due to nutrient imbalance, water stress, pest attack, or extreme temperatures. Lack of boron and potassium can also cause this issue. Maintaining balanced nutrition, proper irrigation, and pest control helps reduce flower drop and improve fruit set.'),(25,'improve soil health','How can I improve soil health over time?','Soil health improves by adding organic manure, compost, and green manure crops. Crop rotation and reduced chemical fertilizer usage help maintain soil fertility. Healthy soil supports better root growth, nutrient absorption, and sustainable farming.'),(26,'nitrogen deficiency symptoms','What are the signs of nitrogen deficiency in crops?','Nitrogen deficiency causes pale green or yellow leaves, slow growth, and reduced tillering. Older leaves are affected first. Applying nitrogen fertilizers in split doses at the right growth stage helps correct this deficiency.'),(27,'protect crop weather','How can I protect my crop from sudden weather changes?','Sudden weather changes such as heavy rain or heat waves stress crops. Using proper drainage, mulching, and selecting climate-resilient crop varieties can reduce damage. Timely advisory from experts helps farmers take preventive measures.'),(28,'uneven crop growth','Why is my crop growing unevenly in the field?','Uneven crop growth may be due to uneven seed distribution, poor land leveling, nutrient imbalance, or irregular irrigation. Proper land preparation, uniform sowing, and balanced fertilizer application help ensure even crop growth.'),(29,'pest spread crops','How do pests spread quickly in crops?','Pests spread rapidly due to favorable weather conditions, continuous cropping, and lack of early detection. Dense planting and excess fertilizer also encourage pest growth. Regular monitoring and integrated pest management practices help control pest spread.'),(30,'technology agriculture farming','How can technology help me become a better farmer?','Technology helps farmers by providing timely information, expert guidance, and AI-based recommendations. Digital platforms help in disease detection, fertilizer planning, collaboration with other farmers, and access to verified information. Using technology improves productivity, reduces losses, and increases confidence in decision-making.');
/*!40000 ALTER TABLE `chatbot_knowledge` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cropprices`
--

DROP TABLE IF EXISTS `cropprices`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cropprices` (
  `crop_name` varchar(50) DEFAULT NULL,
  `price` varchar(20) DEFAULT NULL,
  `price_date` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cropprices`
--

LOCK TABLES `cropprices` WRITE;
/*!40000 ALTER TABLE `cropprices` DISABLE KEYS */;
INSERT INTO `cropprices` VALUES ('Paddy','2000','2026-02-20'),('Wheat','2500','2026-02-20'),('Millets','3500','2026-02-20'),('Ground Nuts','3000','2026-02-20');
/*!40000 ALTER TABLE `cropprices` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `experts`
--

DROP TABLE IF EXISTS `experts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `experts` (
  `username` varchar(30) NOT NULL,
  `password` varchar(30) DEFAULT NULL,
  `contact` varchar(12) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `qualification` varchar(255) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `approve` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `experts`
--

LOCK TABLES `experts` WRITE;
/*!40000 ALTER TABLE `experts` DISABLE KEYS */;
INSERT INTO `experts` VALUES ('Anil Reddy','Anil@123','9876543210','anilreddy@gmail.com','Plot No. 45, Banjara Hills, Hyderabad, Telangana - 500034','PhD in Agricultural Extension, PJTSAU Hyderabad','Agricultural extension specialist with 12+ years of experience in farmer advisory services, crop management, and government agriculture programs. Passionate about empowering farmers with scientific and sustainable practices.','Approved'),('Meera','Meera@123','9123456780','meera@gmail.com','2-14-89, Vidyanagar Colony, Warangal, Telangana - 506001','M.Sc. in Agronomy, ANGRAU Guntur','Agronomist specializing in soil fertility management, crop productivity enhancement, and climate-resilient agriculture. Experienced in training farmers on modern cultivation techniques.','Approved');
/*!40000 ALTER TABLE `experts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `farmers`
--

DROP TABLE IF EXISTS `farmers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `farmers` (
  `username` varchar(30) NOT NULL,
  `password` varchar(30) DEFAULT NULL,
  `contact` varchar(12) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `intrested_crops` varchar(500) DEFAULT NULL,
  `approve` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `farmers`
--

LOCK TABLES `farmers` WRITE;
/*!40000 ALTER TABLE `farmers` DISABLE KEYS */;
INSERT INTO `farmers` VALUES ('Mahesh','Mahesh@123','9866123456','mahesh@gmail.com','3-22, Lingampet Village, Nizamabad, Telangana','Wheat','Approved'),('Raju','Raju@123','9398123456','raju@gmail.com','7-14, Bhainsa Area, Adilabad, Telangana','Wheat','Approved'),('Ramesh','Ramesh@123','9849123456','ramesh@gmail.com','H.No 2-45, Kothapally Village, Karimnagar, Telangana','Paddy','Approved'),('Srinivas','Srinivas@123','9701234567','srinivas@gmail.com','5-89, Ghanpur Mandal, Warangal Rural, Telangana','Paddy','Approved');
/*!40000 ALTER TABLE `farmers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guides`
--

DROP TABLE IF EXISTS `guides`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `guides` (
  `expert_name` varchar(30) DEFAULT NULL,
  `guide_description` varchar(600) DEFAULT NULL,
  `filename` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guides`
--

LOCK TABLES `guides` WRITE;
/*!40000 ALTER TABLE `guides` DISABLE KEYS */;
INSERT INTO `guides` VALUES ('Meera','Practical Crop Production Guide (ICAR)\r\nThis guide provides comprehensive technical recommendations for scientific rice cultivation under Indian agro-climatic conditions. It covers land preparation, seed selection, nursery management, transplanting techniques, nutrient management, water-saving irrigation methods, integrated pest and disease control, and post-harvest handling practices. The guide is designed to help farmers improve productivity, reduce input costs, and adopt sustainable rice production practices aligned with ICAR recommendations.','practical-crop-production.pdf'),('Anil Reddy','Wheat Cultivation Practices – ICAR Guide\r\nThis document outlines best practices for wheat cultivation including improved varieties, optimal sowing time, seed treatment, fertilizer scheduling, irrigation management, and weed control measures. The guide also provides strategies for managing major wheat pests and diseases such as rust and aphids. It is intended to assist farmers in achieving higher yields and maintaining grain quality through scientifically validated agronomic techniques.','wheat practices.pdf');
/*!40000 ALTER TABLE `guides` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `query`
--

DROP TABLE IF EXISTS `query`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `query` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `farmer_name` varchar(30) DEFAULT NULL,
  `query` varchar(600) DEFAULT NULL,
  `response` varchar(1000) DEFAULT NULL,
  `query_date` varchar(30) DEFAULT NULL,
  `expert_name` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `query`
--

LOCK TABLES `query` WRITE;
/*!40000 ALTER TABLE `query` DISABLE KEYS */;
INSERT INTO `query` VALUES (1,'Ramesh','My wheat crop (45 days old) is showing yellowing of lower leaves. Soil is loamy and irrigation is normal. Weather has been cloudy for the past week. Yellowing is spreading slowly across the field.','This symptom indicates nitrogen deficiency. Apply urea (25–30 kg/acre) through irrigation immediately. Also ensure proper drainage because cloudy weather can slow nitrogen uptake.','2026-02-20','Anil Reddy'),(2,'Ramesh','Paddy crop (tillering stage) has small brown spots that are increasing. Humidity is high due to continuous rains.','This is likely leaf blast disease. Spray Tricyclazole 0.6 g/litre at 7-day intervals. Avoid excessive nitrogen fertilizer and maintain field sanitation.  ','2026-02-20','Anil Reddy'),(3,'Ramesh','Cotton crop is shedding young bolls. Soil is black cotton soil and temperature is very high this month.','Pending','2026-02-20',NULL),(4,'Srinivas','Tomato plants are showing upward leaf curling and slow growth. Whiteflies are visible on leaves.','This is Tomato Leaf Curl Virus spread by whiteflies. Spray Imidacloprid 0.3 ml/litre and remove severely infected plants to prevent spread.      ','2026-02-20','Anil Reddy');
/*!40000 ALTER TABLE `query` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schemes`
--

DROP TABLE IF EXISTS `schemes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `schemes` (
  `policy_name` varchar(100) DEFAULT NULL,
  `policy_desc` varchar(1000) DEFAULT NULL,
  `info_type` varchar(30) DEFAULT NULL,
  `info_date` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schemes`
--

LOCK TABLES `schemes` WRITE;
/*!40000 ALTER TABLE `schemes` DISABLE KEYS */;
INSERT INTO `schemes` VALUES ('Pradhan Mantri Fasal Bima Yojana (PMFBY)','Pradhan Mantri Fasal Bima Yojana is a flagship crop insurance scheme launched in 2016 to protect farmers from crop losses due to natural calamities, pests, and diseases. The scheme provides financial support and ensures income stability by offering insurance coverage for food crops, oilseeds, and commercial crops. It encourages farmers to adopt modern agricultural practices while reducing their premium burden. ','Scheme','2026-02-20'),('Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)','PM-KISAN is a central government income support scheme providing financial assistance to eligible farmer families. Under this scheme, farmers receive direct income transfers annually to help meet agricultural input costs and household needs. It aims to improve farmers’ financial security and support small and marginal farmers.','Scheme','2026-02-20'),('Pradhan Mantri Krishi Sinchai Yojana (PMKSY)','PMKSY is a national mission launched to improve farm productivity through efficient irrigation and water resource management. The scheme promotes micro-irrigation, water conservation, and “Per Drop More Crop” practices to enhance water use efficiency and boost agricultural output. ','Scheme','2026-02-20');
/*!40000 ALTER TABLE `schemes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-13 13:44:44
