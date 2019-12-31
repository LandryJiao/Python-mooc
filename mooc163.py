import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from bs4 import BeautifulSoup as BS
import csv,time

def Chrome_web(url):
	#谷歌浏览器爬取
	driver = webdriver.Chrome()  
	driver.set_page_load_timeout(1000)  
	driver.get(url)  
	# driver.maximize_window() # 将浏览器最大化显示  
	driver.implicitly_wait(2) # 控制间隔时间，等待浏览器反应
	return driver
	
def crawl_mooc(subjects):
	url = 'http://www.icourse163.org/category/all'
	driver=Chrome_web(url) # 模拟打开浏览器 
	for subject in subjects:
		subject_Eng=subjects[subject]

		# 模拟点击科目
		ele=driver.find_element_by_link_text(subject)
		ele.click()
		time.sleep(2)

		# 关闭弹窗
		try:
			driver.find_element_by_xpath(".//*[@class='u-icon u-icon-close']").click()
		except:
			pass

		# # 模拟点击已结束
		driver.find_element_by_xpath(".//*[@class='f-fl ga-click']").click()
		time.sleep(2)

		class_page_num,class_max_page_num=1,1
		# 课程翻页
		while(True):
			if class_page_num>100 or class_page_num>class_max_page_num:    #设置爬取页数
				print('已爬取MOOC'+subject+'课程'+str(class_page_num-1)+'页！')
				break
			htm_const = driver.page_source  
			soup = BS(htm_const,'xml')
			if class_page_num==1:
				class_max_page_num=int(soup.find_all(name='a',attrs={'class':'th-bk-main-gh'})[-2].string)
			# 单页课程遍历，每页20门课程
			jishu = 0
			while(jishu<=19):
				jishu = jishu + 1

			## 模拟点击课程
				driver.find_element_by_xpath(".//*[@class='u-clist f-bgw f-cb f-pr j-href ga-click'][{}]".format(jishu)).click()
				time.sleep(2)

				# 获取网页句柄
				windows = driver.window_handles
				driver.switch_to.window(windows[1])

				# 确定课程是否存在
				NowURL = driver.current_url
				if NowURL == 'https://www.icourse163.org/':
					driver.close()
					windows = driver.window_handles
					driver.switch_to.window(windows[0])
					continue

				# 模拟点击关闭
				try:
					driver.find_element_by_xpath(".//span[@class='zcls']").click()
				except:
					pass

				html_const = driver.page_source  # 获取当前网页源码
				soup = BS(html_const,'xml')
				# print(soup)

				# 获取课程ID
				NowURL=driver.current_url
				c_ID= NowURL.replace('http://www.icourse163.org/course/','')
				# print(NowURL)

				# 获取采集时间
				Nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

				# 获取每项信息
				c_names=driver.find_element_by_xpath(".//*[@class='course-title f-ib f-vam']").text
				c_schedule=driver.find_element_by_xpath(".//*[@class='course-enroll-info_course-info']").text
				c_schedule=re.sub('\n','',c_schedule)
				c_schedule=re.sub(' ','',c_schedule)
				# 已参加人数
				c_join=driver.find_element_by_xpath(".//*[@class='course-enroll-info_course-enroll_price-enroll_enroll-count']").text
				
				# 教师信息
				c_teachers_ID=soup.find('div',class_='m-teachers_teacher-list')
				c_teachers_ID_list=c_teachers_ID.find_all('a')
				c_teachers=soup.find_all('h3',class_='f-fc3')
				c_teachers_info=""
				for j,k in zip(c_teachers,c_teachers_ID_list):
					c_teachers_info=c_teachers_info+j.get_text()+k.get('href')
					c_teachers_info = re.sub('\n','',c_teachers_info)
					# print(c_teachers_info)

				# 课程概述
				c_summarize=soup.find('div',class_='f-richEditorText').get_text()
				# 过滤特殊字符
				c_summarize=re.sub('\xa0','',c_summarize)
				c_summarize=re.sub('\n','',c_summarize)
				c_summarize=re.sub(' ','',c_summarize)
				c_summarize=re.sub('[paɪθən]','',c_summarize)
				c_summarize=re.sub('•','',c_summarize)
				c_summarize=re.sub('\u200d','',c_summarize)
				c_summarize=re.sub('\xd8','',c_summarize)
				c_summarize=re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]',',',c_summarize)
				c_summarize=re.sub(r',{2,}', ',',c_summarize,re.S)#删除重复‘,‘
				kc_info=[subject,c_names, c_ID, c_schedule, c_join, c_teachers_info, c_summarize, Nowtime]
				print(c_names)
				time.sleep(2)

				# 写入文件TXT
				# with open('F:\\mooc\\mooc.txt','a+',encoding='utf-8') as f:
				#   f.write(c_names+'\n'+c_schedule+'\n'+c_join+'\n'+c_teachers_info+'\n'+c_summarize+'\n\n')

				strContent = []
				for i in kc_info:
					strContent.append(i)
				# 写入文件CSV
				with open("F:\\mooc\\mooc.csv",'a+', newline='') as csvfile:
					f=csv.writer(csvfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
					f.writerow(strContent)

				## 爬取评论
				# 模拟点击课程评论
				driver.find_element_by_id("review-tag-button").click()
				page_num,max_page_num=1,1
				while(True):
					if page_num>max_page_num:    #设置爬取页数
						print('已爬取MOOC课程'+str(page_num-1)+'页！')
						break
					htm_const = driver.page_source  
					soup = BS(htm_const,'xml')
					try:
						if page_num==1:
							max_page_num=int(soup.find_all(name='a',attrs={'class':'th-bk-main-gh'})[-2].string)
					except:
						pass
					# 获取星级
					try:
						c_star=driver.find_element_by_xpath(".//*[@class='ux-mooc-comment-course-comment_head_rating-scores']").text
					except:
						c_star="暂无总评"
					# 获取评价总数
					try:
						c_evaluateNum = driver.find_element_by_xpath(".//*[@class='ux-mooc-comment-course-comment_head_rating-action_tips']").text
					except:
						c_evaluateNum = "评价人数不足"
					# 获取用户ID链表
					c_user_ID_list = driver.find_elements_by_xpath(".//*[@class='primary-link ux-mooc-comment-course-comment_comment-list_item_body_user-info_name']")
					# 获取用户评星
					try:
						c_user_list = driver.find_elements_by_xpath(".//*[@class='ux-mooc-comment-course-comment_comment-list_item']")
						c_user_star_listNum = []
						for k in c_user_list:
							c_user_star_list = k.find_elements_by_xpath(".//*[@class='star ux-icon-custom-rating-favorite']")
							c_user_star_listNum.append(len(c_user_star_list))
					
						# 获取用户评论链表
						c_user_evaluate_list = driver.find_elements_by_xpath(".//*[@class='ux-mooc-comment-course-comment_comment-list_item_body_content']")
						# 获取用户评论时间和赞
						c_user_time_and_good_list = driver.find_elements_by_xpath(".//*[@class='ux-mooc-comment-course-comment_comment-list_item_body_comment-info']")
						kc_user_info=[c_names, c_ID, c_star, c_evaluateNum]
						# print(c_names, c_ID, c_star, c_evaluateNum, c_user_ID, c_user_time_and_good)
					except:
						c_user_list = driver.find_elements_by_xpath(".//*[@class='ux-mooc-comment-course-comment_comment-list_item']")
						c_user_star_listNum = []
						for k in c_user_list:
							c_user_star_list = k.find_elements_by_xpath(".//*[@class='star ux-icon-custom-rating-favorite']")
							c_user_star_listNum.append(len(c_user_star_list))
					
						# 获取用户评论链表
						c_user_evaluate_list = driver.find_elements_by_xpath(".//*[@class='ux-mooc-comment-course-comment_comment-list_item_body_content']")
						# 获取用户评论时间和赞
						c_user_time_and_good_list = driver.find_elements_by_xpath(".//*[@class='ux-mooc-comment-course-comment_comment-list_item_body_comment-info']")
						kc_user_info=[c_names, c_ID, c_star, c_evaluateNum]
						# print(c_names, c_ID, c_star, c_evaluateNum, c_user_ID, c_user_time_and_good)
					for j,k,l,m in zip(c_user_ID_list,c_user_star_listNum,c_user_evaluate_list,c_user_time_and_good_list):
						strContent = []
						for i in kc_user_info:
							strContent.append(i)
						strContent.append(j.text)
						new_j = j.get_attribute("href")
						j = re.sub('http://www.icourse163.org/home.htm?user','',new_j)
						strContent.append(j)
						strContent.append(k)
						strContent.append(l.text)
						m_text = m.text
						new_m = re.sub('\n','',m_text)
						new_m_list = new_m.split("开课")
						c_user_time = new_m_list[0]
						c_user_good = new_m_list[1]
						strContent.append(c_user_time+'开课')
						strContent.append(c_user_good)
						# 写入各门课程文件CSV
						with open("F:\\mooc\\mooc_"+c_names+"_"+c_ID+"_evaluate.csv",'a+', newline='') as csvfile:
							f=csv.writer(csvfile,delimiter=',',quoting=csv.QUOTE_MINIMAL)
							try:
								f.writerow(strContent)
							except:
								pass
						
					# 点击下一页
					try:  
						next_page = WebDriverWait(driver, 10).until(  
						   EC.visibility_of(driver.find_element_by_link_text('下一页'))
						)  
						next_page.click()  
						time.sleep(1)  
					except Exception as e:  
						print(e)  
						break
					page_num+=1

				# 重新获取句柄
				driver.close()
				windows = driver.window_handles
				driver.switch_to.window(windows[0])

			# 课程翻页
			try:  
				next_page = WebDriverWait(driver, 10).until(  
				   EC.visibility_of(driver.find_element_by_link_text('下一页'))
				)  
				next_page.click()  
				time.sleep(1)  
			except Exception as e:  
				print(e)  
				break
			class_page_num+=1
			
	driver.quit()

def main():
	start_time=time.time()
	subjects={'计算机':'computer','经济管理':'management','心理学':'psychology',
	   '外语':'language','文学历史':'literary_history','艺术设计':'art','工学':'engineering',
	   '理学':'science','医药卫生':'biomedicine','农林园艺':'agriculture','哲学':'philosophy','法学':'law',
	   '教育教学':'teaching_method'}
	# subjects={'法学':'law'}
	crawl_mooc(subjects)
	end_time=time.time()
	print('执行程序一共花了：'+str(end_time-start_time))

if __name__ == '__main__':  
	main()